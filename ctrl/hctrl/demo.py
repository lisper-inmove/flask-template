from ctrl.base_ctrl import BaseCtrl


class DemoCtrl(BaseCtrl):

    def test(self):
        return "Post Test"

    def test_GET(self):
        return "Get Test"

    def test_HEAD(self):
        return "Head Success"

    def weather(self):
        return "Hot"
