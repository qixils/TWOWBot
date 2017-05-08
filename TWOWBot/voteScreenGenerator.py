from PIL import Image, ImageDraw, ImageFont
import random, argparse, re, os, textwrap, json, csv

arial = ImageFont.truetype('./resources/arial.ttf',30)

def parse_args(keylist):
	parser = argparse.ArgumentParser()
	parser.add_argument('input')
	parser.add_argument("-i", "--iterations", nargs='?', const=10, default=10)
	args = parser.parse_args()
	path = args.input
	its=int(args.iterations)
	
	submissions = []
	with open('./{}/responses.csv'.format(path),'r') as csvfile:#read responses
		reader = csv.reader(csvfile,delimiter=',', quotechar='"')
		for row in reader:
			submissions.append(row[1])
			
	keyorder = random.sample(range(len(keylist)),its)
	submissionCount = len(submissions)
	
	return (path,its,submissions,keyorder,submissionCount)
	
def create_random_order(submissions,its,submissionCount):
	voteList = []
	for randomListNumber in range(int(10*its/len(submissions))+1):
	
		randomSubmissionOrder = list(range(submissionCount))
		random.shuffle(randomSubmissionOrder)
		voteList.append(randomSubmissionOrder)
		
	return voteList

		
def wrap_text(text,width):
	lines = textwrap.wrap(text,width)
	new_text='\n'.join(lines)
	return new_text
	
def count_words(text):
	indivWords = re.sub('/[^a-zA-Z0-9 ]/','',text).split(' ')#removes non alphanumeric and space
	count = 0
	for word in indivWords:
		if re.search('[a-zA-Z0-9]',word):#if "word" is not completely spaces
			count +=1
	return count
			

def draw_screens(keylist,path,its,keyorder,voteList,submissionCount,submissions):
	screenDict = {}
	voteNumber = 0
	text_writer = open('./'+path+'/ballots.txt','w')
	for iteration in range(its):

		base = Image.open('./resources/base.png').convert('RGB')
		drawer = ImageDraw.Draw(base)
		existingEntries = []
		
		word = keylist[keyorder[iteration]].upper()
		w = drawer.textsize(word,arial)[0]
		drawer.text((1360-int(w/2), 30), word, font=arial, fill="black")
		
		text_writer.write(word+'\n\n')
		
		for i in range(10):
			
			#ensures all submissions are displayed
			submissionNumber = voteList[int(voteNumber/submissionCount)][voteNumber%submissionCount] 
			while submissionNumber in existingEntries:
				voteList[int(voteNumber/submissionCount)].remove(submissionNumber)
				voteList[int(voteNumber/submissionCount)].append(submissionNumber)
				submissionNumber = voteList[int(voteNumber/submissionCount)][voteNumber%submissionCount]
				
			response = wrap_text(submissions[submissionNumber],85)
			drawer.text((100,71*i+78-drawer.textsize(response,arial)[1]/2), response, font=arial, fill=(0,0,0))
			distance = 130+drawer.textsize(response,arial)[0]
			
			wordCount = count_words(response)
					
			if wordCount >10:
				drawer.text((distance,71*i+60), str(wordCount), font=arial, fill=(255,0,0))#blue
			else:
				drawer.text((distance,71*i+60), str(wordCount), font=arial, fill=(30,30,255))#red
			
			existingEntries.append(submissionNumber)
			ballot_line = ':regional_indicator_{}: {} ({})\n'.format(chr(i+97),submissions[submissionNumber],wordCount)
			text_writer.write(ballot_line)
			
			voteNumber+=1
			
		screenDict[word]=list(existingEntries)
		base.save('./'+path+'/voteScreens/'+str(iteration)+'.png')
		text_writer.write('\n\n\n\n\n')
		
	open('./'+path+'/dict.json','w').write(json.dumps(screenDict))
	
	
def main():
	keylist = open('./resources/words.txt','r').read().split('\n')
	path,its,submissions,keyorder,submissionCount = parse_args(keylist)
	voteList = create_random_order(submissions,its,submissionCount)

	os.makedirs('./'+path+'/voteScreens', exist_ok=True)

	draw_screens(keylist,path,its,keyorder,voteList,submissionCount,submissions)
	
	
if __name__ == '__main__':
	main()
