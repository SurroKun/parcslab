from Pyro4 import expose


class Solver:
    def __init__(self, workers=None, input_file_name=None, output_file_name=None):
        self.input_file_name = input_file_name
        self.output_file_name = output_file_name
        self.workers = workers
        print("Inited")

    def solve(self):
        print("Job Started")
        print("Workers %d" % len(self.workers))

        text = self.read_input()

        step = len(text) // len(self.workers)

        mapped = []
        for i in range(0, len(self.workers)):
            print("map %d" % i)
            mapped.append(self.workers[i].mymap(text[i * step: (i + 1) * step]))

        res = self.myreduce(mapped)

        self.write_output(res)

        print("Job Finished")

    @staticmethod
    @expose
    def mymap(text):
        count = Solver.search(text)

        return count

    @staticmethod
    @expose
    def myreduce(mapped):
        output = 0

        for result in mapped:
            output += result.value

        return output

    def read_input(self):
        file = open(self.input_file_name, 'r')
        data = file.read()
        file.close()
        return data

    def write_output(self, output):
        file = open(self.output_file_name, 'w')
        file.write(str(output))
        file.close()
        print("output done")

    @staticmethod
    def search(txt):
        pat = 'zxc'
        M = len(pat)
        N = len(txt)
        d = 128
        q = 7671453397  # A prime number
        j = 0
        p_hash = 0
        t_hash = 0
        h = 1
        counter = 0
        for i in range(M - 1):
            h = (h * d) % q
        for i in range(M):
            p_hash = (d * p_hash + ord(pat[i])) % q
            t_hash = (d * t_hash + ord(txt[i])) % q
        for i in range(N - M + 1):
            if p_hash == t_hash:
                for j in range(M):
                    if txt[i + j] != pat[j]:
                        break
                j += 1
                if j == M:
                    counter += 1
            if i < N - M:
                t_hash = (d * (t_hash - ord(txt[i]) * h) + ord(txt[i + M])) % q
                if t_hash < 0:
                    t_hash = t_hash + q
        return counter