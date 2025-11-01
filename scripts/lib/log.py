class PrettyLog:
    @staticmethod
    def print(prefix: str, /, *values):
        print(prefix + " ".join(str(value) for value in values))

    @staticmethod
    def info(*values):
        PrettyLog.print("ℹ️  ", *values)

    @staticmethod
    def working(*values):
        PrettyLog.print("⚙️  ", *values)

    @staticmethod
    def done(*values):
        PrettyLog.print("✅ ", *values)

    @staticmethod
    def error(*values):
        PrettyLog.print("⚠️  ", *values)
