""""""
TYPE_CPP2PY = {
    "int64_t": "long long",
    "char": "char",
    "int32_t": "int",
}


class DataTypeGenerator:
    """DataType生成器"""

    def __init__(self, filename: str, prefix: str):
        """Constructor"""
        self.filename = filename
        self.prefix = prefix
        self.enums = {}
        self.last = ""

    def run(self):
        """主函数"""
        self.f_cpp = open(self.filename, "r", encoding='utf8')
        self.f_define = open(f"{self.prefix}_constant.py", "w")
        self.f_typedef = open(f"{self.prefix}_typedef.py", "a+")

        for line in self.f_cpp:
            self.process_line(line)

        self.write()

        self.f_cpp.close()
        self.f_define.close()
        self.f_typedef.close()

        print("DataType生成完毕")

    def process_line(self, line: str):
        """处理每行"""
        line = line.replace("\n", "")
        line = line.split(";")[0]
        line = line.replace("\t", " ")

        if line.startswith("#define"):
            self.process_define(line)
        elif line.startswith("typedef"):
            self.process_typedef(line)
        elif line.startswith("enum"):
            self.process_enum(line)
        elif "= '" in line:
            self.enums[self.last] = "enumchar"

    def process_define(self, line: str):
        """处理常量定义"""
        words = line.split(" ")
        words = [word for word in words if word]
        if len(words) < 3:
            return

        if "=" in words:
            name = words[1]
            value = words[3]
        else:
            name = words[1]
            value = words[2]

        new_line = f"{name} = {value}\n"
        self.f_define.write(new_line)

    def process_enum(self, line: str):
        """处理枚举值定义"""
        words = line.split(" ")
        words = [word for word in words if word]

        name = words[1]

        self.last = name
        self.enums[name] = "enum"

    def process_typedef(self, line: str):
        """处理类型定义"""
        words = line.split(" ")
        words = [word for word in words if word != ""]

        name = words[-1]
        if len(words) > 3:
            typedef = " ".join(words[1:-1])
        else:
            typedef = TYPE_CPP2PY[words[1]]

        if typedef == "char":
            if "[" in name:
                typedef = "string"
                name = name[:name.index("[")]

        new_line = f"{name} = \"{typedef}\"\n"
        self.f_typedef.write(new_line)

    def write(self):
        for k, v in self.enums.items():
            new_line = f"{k} = \"{v}\"\n"
            self.f_typedef.write(new_line)


if __name__ == "__main__":
    generator = DataTypeGenerator("../include/hft/hft_trader_def.h", "hft")
    # generator = DataTypeGenerator("../include/hft/hft_trader_struct.h", "hft")
    generator.run()
