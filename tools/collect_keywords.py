import sys, os
import re

sys.path.append("..")
import utils

def process(file_list):
    print()

    kw_map = dict()

    # 过滤掉常用的大写单词
    stop_words = ["of", "and", "or", "the", "a", "an", "is", "was", "are", "were", "to", "from", "in", "on", "at",
                  "that", "this", "which", "who", "what", "how", "where", "when", "why", "I", "you", "your", "he", "she", "it",
                  "we", "they", "me", "you", "him", "her", "it", "us", "them", "there", "only", "quite", "play", "none", "most",
                  "well", "yeah", "hm", "yeesh", "heh", "wait", "close", "aside", "oh", "right", "um", "nice", "kind", "given",
                  "like", "er", "okay", "especially", "for", "cooking", "indeed", "yes", "then", "really", "very", "much",
                  "do", "does", "hmm", "several", "ha", "not", "some", "would", "except", "uh", "should", "talk", "bug", "no", "self",
                  "black", "truly", "if", "see", "ohh", "perhaps", "consider", "say", "do", "so", "ah", "return", "by", "though",
                  "snap", "but", "by", "come", "listen", "however", "truth", "shall", "let", "god", "someone", "have", "battle",
                  "final", "starting", "start", "follow", "know", "wise", "known", "high", "art", "people", "magic", "must",
                  "could", "forgive", "once", "may", "something", "sometime", "haven", "any", "such", "think", "presenting",
                  "thieves", "thieve", "surely", "usually", "our", "lady", "heart", "half", "hardly", "more", "already", "nothing",
                  "ahh", "good", "now", "careful", "few", "wine", "mm", "precious", "second", "wait", "lack", "as", "yet",
                  "nobody", "bring", "hey", "heya", "elf", "erm", "death", "ye", "thayvians", "one", "strange", "my", "working", "be",
                  "whatever", "anyway", "wizard", "fortunately", "even", "pfeh", "little", "poor", "being", "true",
                  "stranger", "wizards", "shadow", "aye", "rightly", "trust", "cold", "tasks", "still", "distant", "stand",
                  "get", "other", "ancient", "seeking", "secret", "stick", "unless", "until", "tell", "whether", "choose",
                  "nor", "farewell", "did", "after", "with", "believe", "knowing", "welcome", "greetings", "order", "mage",
                  "will", "alright", "thank", "fare", "thanks", "standing", "excellent", "might", "another", "gladly", "time",
                  "go", "actually", "part", "certainly", "hold", "make", "farther", "because", "never", "tragic", "house",
                  "first", "second", "unlikely", "testing", "test", "maybe", "enough", "about", "been", "amused", "just", "hah",
                  "excuse", "successful", "ways", "anything", "begone", "pathetic", "under", "pay", "here", "all", "probably",
                  "regardless", "give", "prelate", "tidings", "ladies", "stay", "thought", "hopefully", "if", "magical", "aid",
                  "ehh", "customs", "these", "twice", "nah", "aww", "normally", "says", "suit", "helm", "great", "experiences",
                  "mistakes", "deeds", "learn", "those", "appearances", "too", "yer", "dear", "danger", "assuming", "take",
                  "cities", "regret", "darker", "glory", "sad", "yours", "mostly", "full", "memories", "please", "noble", "always",
                  "cooler", "proud", "neutrality", "relax", "common", "higher", "obviously", "sometimes", "less", "everything",
                  "according", "better", "huh", "lived", "children", "particularly", "leave", "am", "bah", "show", "shouldn", "tis",
                  "gah", "boo", "whereas", "chaos", "decisive", "body", "eventually", "adding", "mmhm", "distaste", "divine",
                  "freeing", "behold", "dream", "ones", "abandoning", "tonight", "gleaming", "study", "heat", "sand", "divinity",
                  "similar", "eager", "admit", "wild", "worry", "settled", "cleverer", "back", "keep", "neither", "simply", "playing",
                  "care", "trapped", "caution", "considering", "exiling", "powerful", "dark", "stop", "lonely", "living",
                  "convenient", "apology", "able", "strong", "legend", "men", "women", "forget", "terrible", "entertaining",
                  "interesting", "adventure", "heavens", "gate", "their", "longer", "without", "humans", "sitting", "learning", "looking",
                  "fishing", "exactly", "either", "apparently", "master", "almost", "adapting", "ever", "arrogant", "tradition",
                  "beyond", "since", "luck", "troubles", "life", "absolutely", "childhood", "compared", "growing", "illuminating",
                  "bored", "tired", "increasingly", "reality", "chidish", "worthy", "magically", "honor", "run", "suffice", "everyone",
                  "every", "followed", "personality", "difficult", "orders", "three", "two", "his", "her", "can", "things", "both",
                  "unfortunately", "monks", "paladins", "druids", "mages", "soon", "Intriguing", "worked", "far", "power",
                  "myself", "new", "destiny", "mortality", "isolated", "domination"]

    filled_words = ["if", "by", "about", "as", "eventually", "with"]

    for file in file_list:
        lines = utils.read_file(file)
        for line in lines:
            line = pre_procedure(line)
            pick_list = pick(line)
            if len(pick_list) != 0:
                for k in pick_list:
                    if k.lower() in stop_words:
                        continue
                    lk = k.lower()
                    flg = True
                    for f in filled_words:
                        if lk.find(f+' ') != -1:
                            flg = False
                            break
                    if flg:
                        kw_map[k] = 1

    for k in kw_map:
        print(k)

def pre_procedure(sentence):
    # 去除两端空格
    sentence = sentence.strip()
    # 忽略空行
    if sentence == '':
        return ''

    # 提取~~中间部分
    if sentence.find('@') != -1:
        st = sentence.find('~')
        ed = sentence.find('~', st + 1)
        sentence = sentence[st + 1:ed]
    else:
        if sentence.find('~') != -1:
            ed = sentence.find('~') != -1
            sentence = sentence[:ed]
    # 去除 []
    while (sentence.find('[') != -1 and sentence.find(']') != -1):
        st = sentence.find('[')
        ed = sentence.find(']')
        if st != 0:
            sentence = sentence[:st] + sentence[ed+1:]
        else:
            sentence = sentence[ed + 1:]

    # 去除 <>
    while (sentence.find('<') != -1 and sentence.find('>') != -1):
        st = sentence.find('<')
        ed = sentence.find('>')
        if st != 0:
            sentence = sentence[:st] + sentence[ed + 1:]
        else:
            sentence = sentence[ed + 1:]

    return sentence

def pick(sentence):

    pattern = re.compile(r'((?:[A-Z][a-z]+)+(?: of [A-Z][a-z]+)|(?:[A-Z][a-z]+\s?)+)')

    matches = pattern.findall(sentence)

    upper_case_words = []
    for upper in matches:
        upper_case_words.append(upper.strip())

    return upper_case_words


if __name__ == '__main__':

    file_list = []
    direct_path = 'Evandra/tra/'
    files = os.listdir('../Evandra/tra/')
    for file in files:
        if file.lower().find('.tra') != -1:
            file_list.append(direct_path+file)
    process(file_list=file_list)
    # print(pick('The quick brown fox jumps Aaa aa Throne of Bhaal Laa over the lazy dog. Aaa Bbb Ccc'))