#######################################################################################################
# Import

import os, argparse, asyncio, logging, tempfile, json
from datetime import datetime
# grpcio package
import grpc
from grpc import RpcError
# google-auth package
import google.auth as gcp_auth
import google.auth.transport.requests as gcp_auth_req
import google.auth.transport.grpc as gcp_auth_grpc
# my package
import sdklog
from comedia.cowave import CoWave, wave
# proto base
from gcp.cloud.speech.v2.locations_metadata_pb2 import LocationsMetadata
from gcp.longrunning.operations_pb2 import Operation
from gcp.protobuf.timestamp_pb2 import Timestamp
from gcp.protobuf.duration_pb2 import Duration
# proto tts package
import service.gcp_tts_v1_pb2_grpc as tts_v1_grpc
import service.gcp_tts_v1_pb2 as tts_v1
# proto asr package
import service.gcp_locations_pb2_grpc as gcp_location_grpc
import service.gcp_locations_pb2 as gcp_location
import service.gcp_asr_v2_pb2_grpc as asr_v2_grpc
import service.gcp_asr_v2_pb2 as asr_v2

#######################################################################################################
# Define

GCP_AUTH_URL = 'https://www.googleapis.com/auth/cloud-platform'

GCP_TTS_REMOTE = 'texttospeech.googleapis.com:443'
GCP_TTS_CODEC = tts_v1.AudioEncoding.MULAW
GCP_TTS_LANG = ['zh-TW', 'en-US']
GCP_TTS_HERTZ = 8000
GCP_TTS_SPK_RATE = 0.75

GCP_ASR_REMOTE = 'speech.googleapis.com:443'
GCP_ASR_LANG = ['cmn-Hant-TW', 'en-US']
GCP_ASR_LOCATE_FORCE_GLOBAL = True
GCP_ASR_LOCATE = 'asia-southeast1'
GCP_ASR_MODEL = 'chirp_2'

GCP_RECOGNIZER_NAME = 'recognizer'

LOG_LEVEL = logging.DEBUG
LOGGER: logging.Logger

#######################################################################################################
# Utility

def print_exception(name: str, e: Exception, warn=False):
    if isinstance(e, RpcError):
        msg = f'{name} -> gRPC.{e.code()}: {e.details()}'
        if warn:
            LOGGER.warning(msg)
        else:
            LOGGER.error(msg)
        return
    LOGGER.error(f"{str(e)}")

def create_grpc_channel(cred_filename: str, auth_url: str, target_url: str) -> grpc.Channel:
    # Get credentials
    credentials, _ = gcp_auth.load_credentials_from_file(cred_filename, scopes=[auth_url])
    # Get an HTTP request function to refresh credentials
    req = gcp_auth_req.Request()
    # Create a channel
    channel = gcp_auth_grpc.secure_authorized_channel(credentials, req, target_url)
    return channel

def timestamp_pb2_to_str(ts: Timestamp) -> str:
    date_null = 'null'
    return f'{datetime.fromtimestamp(ts.seconds).strftime("%Y-%m-%d %H:%M:%S") if ts.seconds > 0 else date_null}'

def gcp_speech_event_name(event: int) -> str:
    if event == 0:
        return 'UNSPECIFIED'
    if event == 1:
        return 'END_OF_SINGLE_UTTERANCE'
    if event == 2:
        return 'ACTIVITY_BEGIN'
    if event == 3:
        return 'ACTIVITY_END'
    return 'UNKNOWN'

def gcp_duration_sec(duration: Duration) -> float:
    msec = duration.nanos // 1000000
    return duration.seconds + (msec / 1000)

#######################################################################################################
# TTS version 1

def gcp_tts_v1_load_voices(response: tts_v1.ListVoicesResponse) -> list[tts_v1.Voice]:
    voices = []
    for voice in response.voices: # 每次迭代 RepeatedField 會阻塞，直到收到下一個 Field
        voices.append(voice)
        name = voice.name
        lang = voice.language_codes
        gender = voice.ssml_gender
        hertz = voice.natural_sample_rate_hertz
        LOGGER.debug(f"ID={name}; Language={lang}; Gender={gender}; Hertz={hertz};")
    return voices

def gcp_tts_v1_streaming(channel: grpc.Channel, lang_code: str, codec: tts_v1.AudioEncoding, output_path: str):
    # Use the channel to create a stub
    stub = tts_v1_grpc.TextToSpeechStub(channel)
    # Query voice list -----------------------------------------------------------------------
    request = tts_v1.ListVoicesRequest(language_code=lang_code)
    response = stub.ListVoices(request)
    voices = gcp_tts_v1_load_voices(response)
    default_voice_name = ''
    for voice in voices:
        default_voice_name = voice.name
        if lang_code in voice.language_codes:
            if 'Chirp-HD' in voice.name:
                # Google streaming only support Chirp-HD (en-US)
                LOGGER.warning(f'Force voice model into {voice.name}')
                break
    # Synthesizes speech streaming -----------------------------------------------------------
    input_text = tts_v1.StreamingSynthesisInput(text="Hello, Streaming World!")
    voice = tts_v1.VoiceSelectionParams(
        name=default_voice_name,  # Streaming only support Chirp-HD
    )
    audio_config = tts_v1.StreamingAudioConfig(
        audio_encoding=codec,    # Only support PCM, MULAW, ALAW
        sample_rate_hertz=GCP_TTS_HERTZ,
        speaking_rate=GCP_TTS_SPK_RATE
    )
    synth_config = tts_v1.StreamingSynthesizeConfig(
        voice=voice,
        streaming_audio_config=audio_config
    )
    # 這一步是「定義」請求，並未發送數據
    requests = [
        tts_v1.StreamingSynthesizeRequest(streaming_config=synth_config),
        tts_v1.StreamingSynthesizeRequest(input=input_text)
    ]
    try:
        LOGGER.debug('Start StreamingSynthesize')
        responses = stub.StreamingSynthesize(iter(requests)) # 這一步返回「迭代器對象」，尚未發送請求
        output_wav = os.path.join(output_path, 'output.tts.02.wav')
        with wave.open(output_wav, 'wb') as wav_file:
            wav_file.setnchannels(1)
            wav_file.setframerate(GCP_TTS_HERTZ)
            if codec == tts_v1.AudioEncoding.PCM:
                wav_file.setcomptype('NONE', 'not compressed')
                wav_file.setsampwidth(2)
            elif codec == tts_v1.AudioEncoding.ALAW:
                wav_file.setcomptype('ALAW', 'CCITT G.711 a-law')
                wav_file.setsampwidth(1)
            elif codec == tts_v1.AudioEncoding.MULAW:
                wav_file.setcomptype('ULAW', 'CCITT G.711 u-law')
                wav_file.setsampwidth(1)
            # 這一步才真正建立連線，並開始接收流式數據
            for response in responses: # 每次迭代會阻塞，直到收到下一個封包
                LOGGER.debug(f'Received audio content: {len(response.audio_content)} bytes')
                wav_file.writeframes(response.audio_content)
        LOGGER.info(f'音頻已保存至 {output_wav}')
    except Exception as e:
        print_exception('StreamingSynthesize', e)

def gcp_tts_v1(channel: grpc.Channel, lang_code: str, codec: tts_v1.AudioEncoding, output_path: str):
    # Use the channel to create a stub
    stub = tts_v1_grpc.TextToSpeechStub(channel)
    # Query voice list -----------------------------------------------------------------------
    request = tts_v1.ListVoicesRequest(language_code=lang_code)
    response = stub.ListVoices(request)
    gcp_tts_v1_load_voices(response)

    # Synthesizes speech synchronously -------------------------------------------------------
    input_text = tts_v1.SynthesisInput(text="Hello, World!")
    voice = tts_v1.VoiceSelectionParams(
        language_code=lang_code,
        ssml_gender=tts_v1.SsmlVoiceGender.MALE
    )
    if codec == tts_v1.AudioEncoding.PCM:
        codec = tts_v1.AudioEncoding.LINEAR16
    audio_config = tts_v1.AudioConfig(
        audio_encoding=codec,
        sample_rate_hertz=GCP_TTS_HERTZ,
        speaking_rate=GCP_TTS_SPK_RATE
    )
    request = tts_v1.SynthesizeSpeechRequest(
        input=input_text,
        voice=voice,
        audio_config=audio_config
    )
    try:
        response = stub.SynthesizeSpeech(request)
        output_wav = os.path.join(output_path, 'output.tts.01.wav')
        with open(output_wav, 'wb') as out:
            out.write(response.audio_content)
        LOGGER.info(f'音頻已保存至 {output_wav}')
    except Exception as e:
        print_exception('SynthesizeSpeech', e)

#######################################################################################################
# ASR version 2

def gcp_load_locations(response: gcp_location.ListLocationsResponse) -> list[str]:
    locations = []
    for item in response.locations:
        LOGGER.debug(f'{item.name} ({item.location_id})')
        locations.append(item.name)
    return locations

def gcp_load_location_metadata(name: str, res: gcp_location.Location) -> LocationsMetadata | None:
    metadata = res.metadata
    if metadata.type_url != "type.googleapis.com/google.cloud.speech.v2.LocationsMetadata":
        return None
    obj = LocationsMetadata()
    if not metadata.Unpack(obj):
        return None
    LOGGER.info(f'{name} ({res.location_id})')
    for mk, mv in obj.languages.models.items():
        for fk, fv in mv.model_features.items():
            for item in fv.model_feature:
                print(f'{mk}.{fk}.{item.feature}')
        print('-----------------------------------------------------')
    return obj

def gcp_locations_info(channel: grpc.Channel, project_id: str) -> dict[str, LocationsMetadata]:
    lo_dict = {}
    # Use the channel to create a stub
    stub = gcp_location_grpc.LocationsStub(channel)
    request = gcp_location.ListLocationsRequest(name=f'projects/{project_id}')
    try:
        response = stub.ListLocations(request)
        locations = gcp_load_locations(response)
        for location in locations:
            request = gcp_location.GetLocationRequest(name=location)
            response = stub.GetLocation(request)
            locations_metadata = gcp_load_location_metadata(location, response)
            if locations_metadata is not None:
                lo_dict[location] = locations_metadata
    except Exception as e:
        print_exception('ListLocations', e)
    return lo_dict

def gcp_asr_chose_location(location_id: str, lo_dict: dict[str, LocationsMetadata]) -> tuple[str, LocationsMetadata] | tuple[str, None]:
    for k, v in lo_dict.items():
        if location_id in k:
            return k, v
    return '', None

def gcp_asr_chose_model(lang_code: str, model_name: str, data: LocationsMetadata) -> str | None:
    for mk, mv in data.languages.models.items():
        if mk != f'{lang_code}':
            continue
        for fk, fv in mv.model_features.items():
            if fk != f'{model_name}':
                continue
            return fk
    return None

def gcp_print_recognizer(name: str, obj: asr_v2.Recognizer):
    if obj.state == asr_v2.Recognizer.State.STATE_UNSPECIFIED:
        state = 'STATE_UNSPECIFIED'
    elif obj.state == asr_v2.Recognizer.State.ACTIVE:
        state = 'ACTIVE'
    elif obj.state == asr_v2.Recognizer.State.DELETED:
        state = 'DELETED'
    else:
        state = f'STATE_CODE({obj.state})'
    LOGGER.info(f'OperationName: {name}\n'
                f'Recognizer.state = {state}\n'
                f'Recognizer.display_name = "{obj.display_name}"\n'
                f'Recognizer.name = "{obj.name}"\n'
                f'Recognizer.uid = "{obj.uid}"\n'
                f'Recognizer.model = "{obj.model}"\n'
                f'Recognizer.language_codes = {obj.language_codes}\n'
                f'Recognizer.create_time = {timestamp_pb2_to_str(obj.create_time)}\n'
                f'Recognizer.update_time = {timestamp_pb2_to_str(obj.update_time)}\n'
                f'Recognizer.expire_time = {timestamp_pb2_to_str(obj.expire_time)}\n'
                f'Recognizer.delete_time = {timestamp_pb2_to_str(obj.delete_time)}\n'
                f'Recognizer.etag = {obj.etag}\n'
                f'Recognizer.reconciling = "{obj.reconciling}"\n'
                f'Recognizer.kms_key_name = "{obj.kms_key_name}"\n'
                f'Recognizer.kms_key_version_name = "{obj.kms_key_version_name}"')

def gcp_load_recognizer_response(name: str, res: Operation) -> asr_v2.Recognizer | None:
    metadata = res.response
    if metadata.type_url != "type.googleapis.com/google.cloud.speech.v2.Recognizer":
        return None
    obj = asr_v2.Recognizer()
    if not metadata.Unpack(obj):
        return None
    gcp_print_recognizer(name, obj)
    return obj

def gcp_force_location_global(parent: str, flag=GCP_ASR_LOCATE_FORCE_GLOBAL) -> str:
    if flag:
        parts = parent.rsplit("/", 1)
        parent = f'{parts[0]}/global'
        LOGGER.warning(f'Force parent into {parent}')
    return parent

def gcp_create_recognizer_v2(channel: grpc.Channel, parent: str, model: str, wav: CoWave) -> asr_v2.Recognizer | None:
    if parent.endswith('/global'):
        model = 'long'
        LOGGER.warning(f'CreateRecognizer: force model into {model}')
    # Use the channel to create a stub
    stub = asr_v2_grpc.SpeechStub(channel)
    # Set explicit codec configure
    if wav.compression_type == 'ULAW':
        codec = asr_v2.ExplicitDecodingConfig.AudioEncoding.MULAW
    elif wav.compression_type == 'ALAW':
        codec = asr_v2.ExplicitDecodingConfig.AudioEncoding.ALAW
    elif wav.compression_type == 'NONE':
        codec = asr_v2.ExplicitDecodingConfig.AudioEncoding.LINEAR16
    else:
        LOGGER.error(f'CreateRecognizer: unsupported audio encoding')
        return None
    codec_config = asr_v2.ExplicitDecodingConfig(
        encoding=codec,
        sample_rate_hertz=wav.sample_rate,
        audio_channel_count=wav.n_channels
    )
    features = asr_v2.RecognitionFeatures(
        enable_automatic_punctuation=True, # 是否啟用自動標點符號
        enable_spoken_punctuation=False    # 是否取代口述標點符號
    )
    # Set default recognition configure
    recog_config = asr_v2.RecognitionConfig(
        explicit_decoding_config=codec_config,
        language_codes=GCP_ASR_LANG,
        features=features,
        model=model
    )
    # Set recognizer
    recognizer = asr_v2.Recognizer(
        default_recognition_config=recog_config,
        display_name=f'{wav.get_info_name()}-{GCP_RECOGNIZER_NAME}'
    )
    # Set Requester
    request = asr_v2.CreateRecognizerRequest(
        parent=parent,
        recognizer_id=f'{wav.get_info_name()}-{GCP_RECOGNIZER_NAME}',
        validate_only=False,
        recognizer=recognizer
    )
    try:
        res: Operation = stub.CreateRecognizer(request)
        if res.done:
            if res.HasField('error'):
                status = res.error
                LOGGER.error(f'create_recognizer_v2({res.name}): code={status.code}, message={status.message}')
                return None
            return gcp_load_recognizer_response(res.name, res)
        LOGGER.warning(f'create_recognizer_v2({res.name}): In progress.')
    except Exception as e:
        print_exception('CreateRecognizer', e)
    return None

def gcp_get_recognizer_v2(channel: grpc.Channel, parent: str, wav: CoWave) -> asr_v2.Recognizer | None:
    # Use the channel to create a stub
    stub = asr_v2_grpc.SpeechStub(channel)
    # Set Requester
    request = asr_v2.GetRecognizerRequest(
        name=f'{parent}/recognizers/{wav.get_info_name()}-{GCP_RECOGNIZER_NAME}'
    )
    try:
        response: asr_v2.Recognizer = stub.GetRecognizer(request)
        gcp_print_recognizer('GetRecognizer', response)
        if response.state == asr_v2.Recognizer.State.DELETED:
            LOGGER.warning('The state of recognizer cache is DELETED')
        return response
    except Exception as e:
        print_exception('GetRecognizer', e, True)
    return None

def gcp_delete_recognizer_v2(channel: grpc.Channel, parent: str, wav: CoWave):
    # Use the channel to create a stub
    stub = asr_v2_grpc.SpeechStub(channel)
    # Set Requester
    request = asr_v2.DeleteRecognizerRequest(
        name=f'{parent}/recognizers/{wav.get_info_name()}-{GCP_RECOGNIZER_NAME}',
        validate_only=False, # True for simulate deletion
        allow_missing=False
    )
    try:
        res: Operation = stub.DeleteRecognizer(request)
        if res.done:
            if res.HasField('error'):
                status = res.error
                LOGGER.error(f'delete_recognizer_v2({res.name}): code={status.code}, message={status.message}')
                return
            LOGGER.info(f'delete_recognizer_v2({res.name}): DONE ')
            return
        LOGGER.warning(f'delete_recognizer_v2({res.name}): In progress.')
    except Exception as e:
        print_exception('DeleteRecognizer', e, True)

def gcp_asr_v2_streaming(channel: grpc.Channel, recognizer: asr_v2.Recognizer, wav: CoWave):
    # Use the channel to create a stub
    stub = asr_v2_grpc.SpeechStub(channel)
    # Set requests for audio chunk
    requests = []
    for chunk in wav.get_chunks(1024):
        requests.append(asr_v2.StreamingRecognizeRequest(
            recognizer=recognizer.name,
            audio=chunk
        ))
    try:
        LOGGER.debug('Start StreamingRecognize')
        responses = stub.StreamingRecognize(iter(requests)) # 這一步返回「迭代器對象」，尚未發送請求
        for response in responses:  # 每次迭代會阻塞，直到收到下一個封包
            res: asr_v2.StreamingRecognizeResponse = response
            offset_sec = gcp_duration_sec(res.speech_event_offset)
            metadata = res.metadata
            print(f'[event:{gcp_speech_event_name(res.speech_event_type)}] @ {offset_sec:.2f}-sec')
            for result in res.results:
                end_offset = gcp_duration_sec(result.result_end_offset)
                # Find a max confidence of transcript
                confidence = 0.0
                alternative = result.alternatives[0]
                for item in result.alternatives:
                    if item.confidence >= confidence:
                        confidence = item.confidence
                        alternative = item
                # Print result
                transcript = alternative.transcript
                print(f'[{result.language_code}]'
                      f'[ch_tag={result.channel_tag}, end_ts={end_offset:.2f}-sec, confidence={confidence:.2f}, final={result.is_final}] '
                      f'{transcript}'
                )
    except Exception as e:
        print_exception('StreamingRecognize', e)

#######################################################################################################
# Main

def main_chk_output_path(arg) -> str:
    if os.path.exists(arg.output):
        return arg.output
    return tempfile.gettempdir()

def main_chk_cred_file(arg) -> bool:
    if arg.run == 'tts' or arg.run == 'asr':
        rtn = os.path.exists(arg.cred)
        if not rtn:
            LOGGER.critical(f'Cannot found: {arg.cred}')
        return rtn
    return True

def main_get_cred_prj_id(filename: str) -> str | None:
    if not os.path.exists(filename):
        return None
    with open(filename, 'r', encoding='utf-8') as file:
        data = json.load(file)
    if 'project_id' in data:
        value = data['project_id']
        if isinstance(value, str):
            return value
    return None

def main_get_wave(filename: str) -> CoWave | None:
    obj = CoWave(filename)
    if obj.is_valid():
        obj.print_info()
        return obj
    return None

async def main(arg):
    output_path = main_chk_output_path(arg)
    if not main_chk_cred_file(arg):
        LOGGER.error('Cannot open credential JSON file')
        exit(0)
    if arg.run == 'tts':
        channel = create_grpc_channel(arg.cred, GCP_AUTH_URL, GCP_TTS_REMOTE)
        gcp_tts_v1_streaming(channel, GCP_TTS_LANG[1], GCP_TTS_CODEC, output_path)
        gcp_tts_v1(channel, GCP_TTS_LANG[0], GCP_TTS_CODEC, output_path)
    elif arg.run == 'asr':
        prj_id = main_get_cred_prj_id(arg.cred)
        if prj_id is None:
            LOGGER.error('Cannot load project ID from credential JSON file')
            exit(0)
        wav = main_get_wave(arg.wave)
        if wav is None:
            LOGGER.error('Cannot load WAVE file')
            exit(0)
        # Get location data
        channel = create_grpc_channel(arg.cred, GCP_AUTH_URL, GCP_ASR_REMOTE)
        lo_dict = gcp_locations_info(channel, prj_id)
        parent, data = gcp_asr_chose_location(GCP_ASR_LOCATE, lo_dict)
        if data is None:
            LOGGER.error(f'Cannot find location: {GCP_ASR_LOCATE}')
            exit(0)
        # Check model is exist
        for lang in GCP_ASR_LANG:
            val =  gcp_asr_chose_model(lang, GCP_ASR_MODEL, data)
            if val is None:
                LOGGER.error(f'Cannot find model: {GCP_ASR_MODEL}')
                exit(0)
        LOGGER.info(f'Chose {parent} as parent, model={GCP_ASR_MODEL}')
        parent = gcp_force_location_global(parent)
        # Check recognizer existed before creating
        recog = gcp_get_recognizer_v2(channel, parent, wav) if arg.cache else None
        if recog is None:
            LOGGER.debug('Recognizer is not found, start create new recognizer')
            recog = gcp_create_recognizer_v2(channel, parent, GCP_ASR_MODEL, wav)
            if recog is None:
                LOGGER.error('Cannot create recognizer')
                exit(0)
        # Call streaming recognizer
        gcp_asr_v2_streaming(channel, recog, wav)
        # Delete recognizer
        if recog.state != asr_v2.Recognizer.State.DELETED:
            gcp_delete_recognizer_v2(channel, parent, wav)
        LOGGER.debug('END of ASR')

def args_parser():
    parser = argparse.ArgumentParser(description='GCP Speech Recognition')
    parser.add_argument('-r', '--run', type=str, required=True, metavar='VALUE',
                        help='Run process (Available value: tts, asr)')
    parser.add_argument('-c', '--cred', type=str, required=False, metavar='JSON_FILE', default='',
                        help='Give a *.json credential file for GCP')
    parser.add_argument('-w', '--wave', type=str, required=False, metavar='WAVE_FILE', default='',
                        help='Give a *.wav file as input for ASR')
    parser.add_argument('-o', '--output', type=str, required=False, metavar='PATH', default='',
                        help='Give an output path for TTS')
    parser.add_argument('--cache', action='store_true', default=False,
                        help='Use cache first for resources')
    return parser.parse_args()

if __name__ == "__main__":
    LOGGER = sdklog.get_root_logger(LOG_LEVEL)
    sdklog.set_colored_logger(LOGGER)
    args = args_parser()
    asyncio.run(main(args))
