from scripts.resource_helper import ResourceHelper


class Helper:

    def do_help(self):
        dolist = [
            ("用户资源操作", ResourceHelper)
        ]
        for index, c in enumerate(dolist):
            print(f"\t {index}. {c[0]}")
        index = self.__get_help_index(len(dolist))
        cls = dolist[index]

    def __get_help_index(self, maxvalue):
        try:
            result = int(input("输入序号: "))
            if result > maxvalue:
                print(f"请输入小于{maxvalue}")
                return self.__get_help_index(maxvalue)
            return result
        except ValueError as ex:
            print(f"{ex}: 请输入数字")
            return self.__get_help_index(maxvalue)


if __name__ == '__main__':
    Helper().do_help()
