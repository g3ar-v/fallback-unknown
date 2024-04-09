from source.core import FallbackSkill


class UnknownSkill(FallbackSkill):
    def __init__(self):
        super(UnknownSkill, self).__init__()

    def initialize(self):
        self.add_event(
            "recognizer_loop:speech.recognition.unknown",
            self.handle_recognition_unknown,
        )
        self.register_fallback(self.handle_fallback, 100)

    def read_voc_lines(self, name):
        with open(self.find_resource(name + ".voc", "vocab")) as f:
            return filter(bool, map(str.strip, f.read().split("\n")))

    def handle_fallback(self, message):
        utterance = message.data["utterance"].lower()

        for i in ["question", "who.is", "why.is"]:
            for l in self.read_voc_lines(i):
                if utterance.startswith(l):
                    self.log.info("Fallback type: " + i)
                    self.speak_dialog(i, data={"remaining": l.replace(i, "")})
                    return True
        self.speak_dialog("unknown")
        return True

    def handle_recognition_unknown(self, message):
        self.speak_dialog("unknown")


def create_skill():
    return UnknownSkill()
