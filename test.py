import os

my_string = "lalala zac link www.google.com"

my_string = my_string.partition("zac link ")[2]

print(my_string)


class LinkManager(object):

    def __init__(self):
        curr_dir = os.path.dirname(os.path.abspath(__file__))
        self.filename = os.path.join(curr_dir, '../../links.txt')

    def add_link(self, link_text):
        with open(self.filename, 'a') as f:
            f.write(link_text.replace("\n", " ")+"\n")
        with open(self.filename, 'r') as f:
            num_lines = sum(1 for line in f)
        return num_lines

    def get_link(self):
        if not os.path.exists(self.filename):
            open(self.filename, 'w').close()
        else:
            with open(self.filename, 'r') as f:
                print(f.readline())
                remaining_file = f.read()
            with open(self.filename, 'w') as f:
                f.write(remaining_file)


# man = LinkManager()

# print(man.add_link("this is my first \n link"))
# man.add_link("this is my ssecond \n link")
# man.add_link("this is my third \n link")

# man.get_link()

msg_text = "nicole:this is my news:again"
tokens = msg_text.partition(":")
for token in tokens:
    print(token)
