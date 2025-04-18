# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: service/gcp_tts_v1.proto
# Protobuf Python Version: 5.29.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    29,
    0,
    '',
    'service/gcp_tts_v1.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from gcp.api import annotations_pb2 as gcp_dot_api_dot_annotations__pb2
from gcp.api import client_pb2 as gcp_dot_api_dot_client__pb2
from gcp.api import field_behavior_pb2 as gcp_dot_api_dot_field__behavior__pb2
from gcp.api import resource_pb2 as gcp_dot_api_dot_resource__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x18service/gcp_tts_v1.proto\x12\x1cgoogle.cloud.texttospeech.v1\x1a\x19gcp/api/annotations.proto\x1a\x14gcp/api/client.proto\x1a\x1cgcp/api/field_behavior.proto\x1a\x16gcp/api/resource.proto\"/\n\x11ListVoicesRequest\x12\x1a\n\rlanguage_code\x18\x01 \x01(\tB\x03\xe0\x41\x01\"I\n\x12ListVoicesResponse\x12\x33\n\x06voices\x18\x01 \x03(\x0b\x32#.google.cloud.texttospeech.v1.Voice\"\x94\x01\n\x05Voice\x12\x16\n\x0elanguage_codes\x18\x01 \x03(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x42\n\x0bssml_gender\x18\x03 \x01(\x0e\x32-.google.cloud.texttospeech.v1.SsmlVoiceGender\x12!\n\x19natural_sample_rate_hertz\x18\x04 \x01(\x05\"d\n\x14\x41\x64vancedVoiceOptions\x12*\n\x1dlow_latency_journey_synthesis\x18\x01 \x01(\x08H\x00\x88\x01\x01\x42 \n\x1e_low_latency_journey_synthesis\"\xdd\x02\n\x17SynthesizeSpeechRequest\x12@\n\x05input\x18\x01 \x01(\x0b\x32,.google.cloud.texttospeech.v1.SynthesisInputB\x03\xe0\x41\x02\x12\x46\n\x05voice\x18\x02 \x01(\x0b\x32\x32.google.cloud.texttospeech.v1.VoiceSelectionParamsB\x03\xe0\x41\x02\x12\x44\n\x0c\x61udio_config\x18\x03 \x01(\x0b\x32).google.cloud.texttospeech.v1.AudioConfigB\x03\xe0\x41\x02\x12W\n\x16\x61\x64vanced_voice_options\x18\x08 \x01(\x0b\x32\x32.google.cloud.texttospeech.v1.AdvancedVoiceOptionsH\x00\x88\x01\x01\x42\x19\n\x17_advanced_voice_options\"\xda\x02\n\x19\x43ustomPronunciationParams\x12\x13\n\x06phrase\x18\x01 \x01(\tH\x00\x88\x01\x01\x12h\n\x11phonetic_encoding\x18\x02 \x01(\x0e\x32H.google.cloud.texttospeech.v1.CustomPronunciationParams.PhoneticEncodingH\x01\x88\x01\x01\x12\x1a\n\rpronunciation\x18\x03 \x01(\tH\x02\x88\x01\x01\"o\n\x10PhoneticEncoding\x12!\n\x1dPHONETIC_ENCODING_UNSPECIFIED\x10\x00\x12\x19\n\x15PHONETIC_ENCODING_IPA\x10\x01\x12\x1d\n\x19PHONETIC_ENCODING_X_SAMPA\x10\x02\x42\t\n\x07_phraseB\x14\n\x12_phonetic_encodingB\x10\n\x0e_pronunciation\"g\n\x14\x43ustomPronunciations\x12O\n\x0epronunciations\x18\x01 \x03(\x0b\x32\x37.google.cloud.texttospeech.v1.CustomPronunciationParams\"\x90\x01\n\x12MultiSpeakerMarkup\x12I\n\x05turns\x18\x01 \x03(\x0b\x32\x35.google.cloud.texttospeech.v1.MultiSpeakerMarkup.TurnB\x03\xe0\x41\x02\x1a/\n\x04Turn\x12\x14\n\x07speaker\x18\x01 \x01(\tB\x03\xe0\x41\x02\x12\x11\n\x04text\x18\x02 \x01(\tB\x03\xe0\x41\x02\"\xea\x01\n\x0eSynthesisInput\x12\x0e\n\x04text\x18\x01 \x01(\tH\x00\x12\x0e\n\x04ssml\x18\x02 \x01(\tH\x00\x12P\n\x14multi_speaker_markup\x18\x04 \x01(\x0b\x32\x30.google.cloud.texttospeech.v1.MultiSpeakerMarkupH\x00\x12V\n\x15\x63ustom_pronunciations\x18\x03 \x01(\x0b\x32\x32.google.cloud.texttospeech.v1.CustomPronunciationsB\x03\xe0\x41\x01\x42\x0e\n\x0cinput_source\"\x95\x02\n\x14VoiceSelectionParams\x12\x1a\n\rlanguage_code\x18\x01 \x01(\tB\x03\xe0\x41\x02\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x42\n\x0bssml_gender\x18\x03 \x01(\x0e\x32-.google.cloud.texttospeech.v1.SsmlVoiceGender\x12\x45\n\x0c\x63ustom_voice\x18\x04 \x01(\x0b\x32/.google.cloud.texttospeech.v1.CustomVoiceParams\x12H\n\x0bvoice_clone\x18\x05 \x01(\x0b\x32..google.cloud.texttospeech.v1.VoiceCloneParamsB\x03\xe0\x41\x01\"\xf1\x01\n\x0b\x41udioConfig\x12H\n\x0e\x61udio_encoding\x18\x01 \x01(\x0e\x32+.google.cloud.texttospeech.v1.AudioEncodingB\x03\xe0\x41\x02\x12\x1d\n\rspeaking_rate\x18\x02 \x01(\x01\x42\x06\xe0\x41\x04\xe0\x41\x01\x12\x15\n\x05pitch\x18\x03 \x01(\x01\x42\x06\xe0\x41\x04\xe0\x41\x01\x12\x1e\n\x0evolume_gain_db\x18\x04 \x01(\x01\x42\x06\xe0\x41\x04\xe0\x41\x01\x12\x1e\n\x11sample_rate_hertz\x18\x05 \x01(\x05\x42\x03\xe0\x41\x01\x12\"\n\x12\x65\x66\x66\x65\x63ts_profile_id\x18\x06 \x03(\tB\x06\xe0\x41\x04\xe0\x41\x01\"\xf1\x01\n\x11\x43ustomVoiceParams\x12\x32\n\x05model\x18\x01 \x01(\tB#\xe0\x41\x02\xfa\x41\x1d\n\x1b\x61utoml.googleapis.com/Model\x12\\\n\x0ereported_usage\x18\x03 \x01(\x0e\x32=.google.cloud.texttospeech.v1.CustomVoiceParams.ReportedUsageB\x05\x18\x01\xe0\x41\x01\"J\n\rReportedUsage\x12\x1e\n\x1aREPORTED_USAGE_UNSPECIFIED\x10\x00\x12\x0c\n\x08REALTIME\x10\x01\x12\x0b\n\x07OFFLINE\x10\x02\"2\n\x10VoiceCloneParams\x12\x1e\n\x11voice_cloning_key\x18\x01 \x01(\tB\x03\xe0\x41\x02\"1\n\x18SynthesizeSpeechResponse\x12\x15\n\raudio_content\x18\x01 \x01(\x0c\"\x9f\x01\n\x14StreamingAudioConfig\x12H\n\x0e\x61udio_encoding\x18\x01 \x01(\x0e\x32+.google.cloud.texttospeech.v1.AudioEncodingB\x03\xe0\x41\x02\x12\x1e\n\x11sample_rate_hertz\x18\x02 \x01(\x05\x42\x03\xe0\x41\x01\x12\x1d\n\rspeaking_rate\x18\x03 \x01(\x01\x42\x06\xe0\x41\x04\xe0\x41\x01\"\x94\x02\n\x19StreamingSynthesizeConfig\x12\x46\n\x05voice\x18\x01 \x01(\x0b\x32\x32.google.cloud.texttospeech.v1.VoiceSelectionParamsB\x03\xe0\x41\x02\x12W\n\x16streaming_audio_config\x18\x04 \x01(\x0b\x32\x32.google.cloud.texttospeech.v1.StreamingAudioConfigB\x03\xe0\x41\x01\x12V\n\x15\x63ustom_pronunciations\x18\x05 \x01(\x0b\x32\x32.google.cloud.texttospeech.v1.CustomPronunciationsB\x03\xe0\x41\x01\"9\n\x17StreamingSynthesisInput\x12\x0e\n\x04text\x18\x01 \x01(\tH\x00\x42\x0e\n\x0cinput_source\"\xce\x01\n\x1aStreamingSynthesizeRequest\x12S\n\x10streaming_config\x18\x01 \x01(\x0b\x32\x37.google.cloud.texttospeech.v1.StreamingSynthesizeConfigH\x00\x12\x46\n\x05input\x18\x02 \x01(\x0b\x32\x35.google.cloud.texttospeech.v1.StreamingSynthesisInputH\x00\x42\x13\n\x11streaming_request\"4\n\x1bStreamingSynthesizeResponse\x12\x15\n\raudio_content\x18\x01 \x01(\x0c*W\n\x0fSsmlVoiceGender\x12!\n\x1dSSML_VOICE_GENDER_UNSPECIFIED\x10\x00\x12\x08\n\x04MALE\x10\x01\x12\n\n\x06\x46\x45MALE\x10\x02\x12\x0b\n\x07NEUTRAL\x10\x03*r\n\rAudioEncoding\x12\x1e\n\x1a\x41UDIO_ENCODING_UNSPECIFIED\x10\x00\x12\x0c\n\x08LINEAR16\x10\x01\x12\x07\n\x03MP3\x10\x02\x12\x0c\n\x08OGG_OPUS\x10\x03\x12\t\n\x05MULAW\x10\x05\x12\x08\n\x04\x41LAW\x10\x06\x12\x07\n\x03PCM\x10\x07\x32\xc7\x04\n\x0cTextToSpeech\x12\x93\x01\n\nListVoices\x12/.google.cloud.texttospeech.v1.ListVoicesRequest\x1a\x30.google.cloud.texttospeech.v1.ListVoicesResponse\"\"\xda\x41\rlanguage_code\x82\xd3\xe4\x93\x02\x0c\x12\n/v1/voices\x12\xbc\x01\n\x10SynthesizeSpeech\x12\x35.google.cloud.texttospeech.v1.SynthesizeSpeechRequest\x1a\x36.google.cloud.texttospeech.v1.SynthesizeSpeechResponse\"9\xda\x41\x18input,voice,audio_config\x82\xd3\xe4\x93\x02\x18\"\x13/v1/text:synthesize:\x01*\x12\x90\x01\n\x13StreamingSynthesize\x12\x38.google.cloud.texttospeech.v1.StreamingSynthesizeRequest\x1a\x39.google.cloud.texttospeech.v1.StreamingSynthesizeResponse\"\x00(\x01\x30\x01\x1aO\xca\x41\x1btexttospeech.googleapis.com\xd2\x41.https://www.googleapis.com/auth/cloud-platformB\xbc\x02\n com.google.cloud.texttospeech.v1B\x11TextToSpeechProtoP\x01ZDcloud.google.com/go/texttospeech/apiv1/texttospeechpb;texttospeechpb\xa2\x02\x04\x43TTS\xaa\x02\x1cGoogle.Cloud.TextToSpeech.V1\xca\x02\x1cGoogle\\Cloud\\TextToSpeech\\V1\xea\x02\x1fGoogle::Cloud::TextToSpeech::V1\xea\x41U\n\x1b\x61utoml.googleapis.com/Model\x12\x36projects/{project}/locations/{location}/models/{model}b\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'service.gcp_tts_v1_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'\n com.google.cloud.texttospeech.v1B\021TextToSpeechProtoP\001ZDcloud.google.com/go/texttospeech/apiv1/texttospeechpb;texttospeechpb\242\002\004CTTS\252\002\034Google.Cloud.TextToSpeech.V1\312\002\034Google\\Cloud\\TextToSpeech\\V1\352\002\037Google::Cloud::TextToSpeech::V1\352AU\n\033automl.googleapis.com/Model\0226projects/{project}/locations/{location}/models/{model}'
  _globals['_LISTVOICESREQUEST'].fields_by_name['language_code']._loaded_options = None
  _globals['_LISTVOICESREQUEST'].fields_by_name['language_code']._serialized_options = b'\340A\001'
  _globals['_SYNTHESIZESPEECHREQUEST'].fields_by_name['input']._loaded_options = None
  _globals['_SYNTHESIZESPEECHREQUEST'].fields_by_name['input']._serialized_options = b'\340A\002'
  _globals['_SYNTHESIZESPEECHREQUEST'].fields_by_name['voice']._loaded_options = None
  _globals['_SYNTHESIZESPEECHREQUEST'].fields_by_name['voice']._serialized_options = b'\340A\002'
  _globals['_SYNTHESIZESPEECHREQUEST'].fields_by_name['audio_config']._loaded_options = None
  _globals['_SYNTHESIZESPEECHREQUEST'].fields_by_name['audio_config']._serialized_options = b'\340A\002'
  _globals['_MULTISPEAKERMARKUP_TURN'].fields_by_name['speaker']._loaded_options = None
  _globals['_MULTISPEAKERMARKUP_TURN'].fields_by_name['speaker']._serialized_options = b'\340A\002'
  _globals['_MULTISPEAKERMARKUP_TURN'].fields_by_name['text']._loaded_options = None
  _globals['_MULTISPEAKERMARKUP_TURN'].fields_by_name['text']._serialized_options = b'\340A\002'
  _globals['_MULTISPEAKERMARKUP'].fields_by_name['turns']._loaded_options = None
  _globals['_MULTISPEAKERMARKUP'].fields_by_name['turns']._serialized_options = b'\340A\002'
  _globals['_SYNTHESISINPUT'].fields_by_name['custom_pronunciations']._loaded_options = None
  _globals['_SYNTHESISINPUT'].fields_by_name['custom_pronunciations']._serialized_options = b'\340A\001'
  _globals['_VOICESELECTIONPARAMS'].fields_by_name['language_code']._loaded_options = None
  _globals['_VOICESELECTIONPARAMS'].fields_by_name['language_code']._serialized_options = b'\340A\002'
  _globals['_VOICESELECTIONPARAMS'].fields_by_name['voice_clone']._loaded_options = None
  _globals['_VOICESELECTIONPARAMS'].fields_by_name['voice_clone']._serialized_options = b'\340A\001'
  _globals['_AUDIOCONFIG'].fields_by_name['audio_encoding']._loaded_options = None
  _globals['_AUDIOCONFIG'].fields_by_name['audio_encoding']._serialized_options = b'\340A\002'
  _globals['_AUDIOCONFIG'].fields_by_name['speaking_rate']._loaded_options = None
  _globals['_AUDIOCONFIG'].fields_by_name['speaking_rate']._serialized_options = b'\340A\004\340A\001'
  _globals['_AUDIOCONFIG'].fields_by_name['pitch']._loaded_options = None
  _globals['_AUDIOCONFIG'].fields_by_name['pitch']._serialized_options = b'\340A\004\340A\001'
  _globals['_AUDIOCONFIG'].fields_by_name['volume_gain_db']._loaded_options = None
  _globals['_AUDIOCONFIG'].fields_by_name['volume_gain_db']._serialized_options = b'\340A\004\340A\001'
  _globals['_AUDIOCONFIG'].fields_by_name['sample_rate_hertz']._loaded_options = None
  _globals['_AUDIOCONFIG'].fields_by_name['sample_rate_hertz']._serialized_options = b'\340A\001'
  _globals['_AUDIOCONFIG'].fields_by_name['effects_profile_id']._loaded_options = None
  _globals['_AUDIOCONFIG'].fields_by_name['effects_profile_id']._serialized_options = b'\340A\004\340A\001'
  _globals['_CUSTOMVOICEPARAMS'].fields_by_name['model']._loaded_options = None
  _globals['_CUSTOMVOICEPARAMS'].fields_by_name['model']._serialized_options = b'\340A\002\372A\035\n\033automl.googleapis.com/Model'
  _globals['_CUSTOMVOICEPARAMS'].fields_by_name['reported_usage']._loaded_options = None
  _globals['_CUSTOMVOICEPARAMS'].fields_by_name['reported_usage']._serialized_options = b'\030\001\340A\001'
  _globals['_VOICECLONEPARAMS'].fields_by_name['voice_cloning_key']._loaded_options = None
  _globals['_VOICECLONEPARAMS'].fields_by_name['voice_cloning_key']._serialized_options = b'\340A\002'
  _globals['_STREAMINGAUDIOCONFIG'].fields_by_name['audio_encoding']._loaded_options = None
  _globals['_STREAMINGAUDIOCONFIG'].fields_by_name['audio_encoding']._serialized_options = b'\340A\002'
  _globals['_STREAMINGAUDIOCONFIG'].fields_by_name['sample_rate_hertz']._loaded_options = None
  _globals['_STREAMINGAUDIOCONFIG'].fields_by_name['sample_rate_hertz']._serialized_options = b'\340A\001'
  _globals['_STREAMINGAUDIOCONFIG'].fields_by_name['speaking_rate']._loaded_options = None
  _globals['_STREAMINGAUDIOCONFIG'].fields_by_name['speaking_rate']._serialized_options = b'\340A\004\340A\001'
  _globals['_STREAMINGSYNTHESIZECONFIG'].fields_by_name['voice']._loaded_options = None
  _globals['_STREAMINGSYNTHESIZECONFIG'].fields_by_name['voice']._serialized_options = b'\340A\002'
  _globals['_STREAMINGSYNTHESIZECONFIG'].fields_by_name['streaming_audio_config']._loaded_options = None
  _globals['_STREAMINGSYNTHESIZECONFIG'].fields_by_name['streaming_audio_config']._serialized_options = b'\340A\001'
  _globals['_STREAMINGSYNTHESIZECONFIG'].fields_by_name['custom_pronunciations']._loaded_options = None
  _globals['_STREAMINGSYNTHESIZECONFIG'].fields_by_name['custom_pronunciations']._serialized_options = b'\340A\001'
  _globals['_TEXTTOSPEECH']._loaded_options = None
  _globals['_TEXTTOSPEECH']._serialized_options = b'\312A\033texttospeech.googleapis.com\322A.https://www.googleapis.com/auth/cloud-platform'
  _globals['_TEXTTOSPEECH'].methods_by_name['ListVoices']._loaded_options = None
  _globals['_TEXTTOSPEECH'].methods_by_name['ListVoices']._serialized_options = b'\332A\rlanguage_code\202\323\344\223\002\014\022\n/v1/voices'
  _globals['_TEXTTOSPEECH'].methods_by_name['SynthesizeSpeech']._loaded_options = None
  _globals['_TEXTTOSPEECH'].methods_by_name['SynthesizeSpeech']._serialized_options = b'\332A\030input,voice,audio_config\202\323\344\223\002\030\"\023/v1/text:synthesize:\001*'
  _globals['_SSMLVOICEGENDER']._serialized_start=3362
  _globals['_SSMLVOICEGENDER']._serialized_end=3449
  _globals['_AUDIOENCODING']._serialized_start=3451
  _globals['_AUDIOENCODING']._serialized_end=3565
  _globals['_LISTVOICESREQUEST']._serialized_start=161
  _globals['_LISTVOICESREQUEST']._serialized_end=208
  _globals['_LISTVOICESRESPONSE']._serialized_start=210
  _globals['_LISTVOICESRESPONSE']._serialized_end=283
  _globals['_VOICE']._serialized_start=286
  _globals['_VOICE']._serialized_end=434
  _globals['_ADVANCEDVOICEOPTIONS']._serialized_start=436
  _globals['_ADVANCEDVOICEOPTIONS']._serialized_end=536
  _globals['_SYNTHESIZESPEECHREQUEST']._serialized_start=539
  _globals['_SYNTHESIZESPEECHREQUEST']._serialized_end=888
  _globals['_CUSTOMPRONUNCIATIONPARAMS']._serialized_start=891
  _globals['_CUSTOMPRONUNCIATIONPARAMS']._serialized_end=1237
  _globals['_CUSTOMPRONUNCIATIONPARAMS_PHONETICENCODING']._serialized_start=1075
  _globals['_CUSTOMPRONUNCIATIONPARAMS_PHONETICENCODING']._serialized_end=1186
  _globals['_CUSTOMPRONUNCIATIONS']._serialized_start=1239
  _globals['_CUSTOMPRONUNCIATIONS']._serialized_end=1342
  _globals['_MULTISPEAKERMARKUP']._serialized_start=1345
  _globals['_MULTISPEAKERMARKUP']._serialized_end=1489
  _globals['_MULTISPEAKERMARKUP_TURN']._serialized_start=1442
  _globals['_MULTISPEAKERMARKUP_TURN']._serialized_end=1489
  _globals['_SYNTHESISINPUT']._serialized_start=1492
  _globals['_SYNTHESISINPUT']._serialized_end=1726
  _globals['_VOICESELECTIONPARAMS']._serialized_start=1729
  _globals['_VOICESELECTIONPARAMS']._serialized_end=2006
  _globals['_AUDIOCONFIG']._serialized_start=2009
  _globals['_AUDIOCONFIG']._serialized_end=2250
  _globals['_CUSTOMVOICEPARAMS']._serialized_start=2253
  _globals['_CUSTOMVOICEPARAMS']._serialized_end=2494
  _globals['_CUSTOMVOICEPARAMS_REPORTEDUSAGE']._serialized_start=2420
  _globals['_CUSTOMVOICEPARAMS_REPORTEDUSAGE']._serialized_end=2494
  _globals['_VOICECLONEPARAMS']._serialized_start=2496
  _globals['_VOICECLONEPARAMS']._serialized_end=2546
  _globals['_SYNTHESIZESPEECHRESPONSE']._serialized_start=2548
  _globals['_SYNTHESIZESPEECHRESPONSE']._serialized_end=2597
  _globals['_STREAMINGAUDIOCONFIG']._serialized_start=2600
  _globals['_STREAMINGAUDIOCONFIG']._serialized_end=2759
  _globals['_STREAMINGSYNTHESIZECONFIG']._serialized_start=2762
  _globals['_STREAMINGSYNTHESIZECONFIG']._serialized_end=3038
  _globals['_STREAMINGSYNTHESISINPUT']._serialized_start=3040
  _globals['_STREAMINGSYNTHESISINPUT']._serialized_end=3097
  _globals['_STREAMINGSYNTHESIZEREQUEST']._serialized_start=3100
  _globals['_STREAMINGSYNTHESIZEREQUEST']._serialized_end=3306
  _globals['_STREAMINGSYNTHESIZERESPONSE']._serialized_start=3308
  _globals['_STREAMINGSYNTHESIZERESPONSE']._serialized_end=3360
  _globals['_TEXTTOSPEECH']._serialized_start=3568
  _globals['_TEXTTOSPEECH']._serialized_end=4151
# @@protoc_insertion_point(module_scope)
