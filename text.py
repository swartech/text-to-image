from PIL import Image
import sys


def get_chars():
    with open('text.txt') as text_file:
        text = [list(line) for line in text_file]
    return text


def merge_all_lines(list):
    result = []
    for sublist in list:
        result.extend(sublist)
    return result


def get_key():
    try:
        with open('key.txt') as key_file:
            key = [list(line) for line in key_file]
            return key[0]
    except IOError:
        print 'Missing: \'key.txt\''
        sys.exit()


def get_encoded_message():
    try:
        im = Image.open("message.png")
        message = list()
        im_message = im.load()
        im_width, im_height = im.size

        for y in xrange(im_height):
            temp = list()
            for x in xrange(im_width):
                imchar = im_message[x, y]
                temp.append(character_key[imchar / 4])
            temp.append('\n')
            message.append(temp)
        message = ''.join(merge_all_lines(message))
        print 'MESSAGE:\n', message
    except IOError:
        print "No encoded message found in \'message.png\'"

character_key = get_key()
get_encoded_message()
text = get_chars()

WIDTH = len(max(text, key=len))
HEIGHT = len(text)
image = list()
display = Image.new('L', (WIDTH, HEIGHT))

for y in xrange(HEIGHT):
    temp = list()
    for x in xrange(len(text[y])):
        try:
            if text[y][x] == '\n':
                while x < WIDTH:
                    temp.append(0)
                    x += 1
            else:
                temp.append(character_key.index(text[y][x]) * 4)
                x += 1
        except ValueError:
            temp.append(0)
    image.append(temp)

display.putdata(merge_all_lines(image))
display.save("text.png")
print "Message from \'text.txt\' saved in \'text.png\'"