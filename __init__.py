# Copyright 2017 Mycroft AI, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from core.skills.core import FallbackSkill


class UnknownSkill(FallbackSkill):
    def __init__(self):
        super(UnknownSkill, self).__init__()

    def initialize(self):
        self.add_event('recognizer_loop:speech.recognition.unknown',
                       self.handle_recognition_unknown)
        self.register_fallback(self.handle_fallback, 100)

    def read_voc_lines(self, name):
        with open(self.find_resource(name + '.voc', 'vocab')) as f:
            return filter(bool, map(str.strip, f.read().split('\n')))

    def handle_fallback(self, message):
        utterance = message.data['utterance'].lower()

        try:
            self.report_metric('failed-intent', {'utterance': utterance})
        except Exception:
            self.log.exception('Error reporting metric')

        for i in ['question', 'who.is', 'why.is']:
            for l in self.read_voc_lines(i):
                if utterance.startswith(l):
                    self.log.info('Fallback type: ' + i)
                    self.speak_dialog(i, data={'remaining': l.replace(i, '')})
                    return True
        self.speak_dialog('unknown')
        return True

    def handle_recognition_unknown(self, message):
        self.speak_dialog('unknown')
        

def create_skill():
    return UnknownSkill()
