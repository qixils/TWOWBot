import ast, argparse, statistics, textwrap, csv, json, os
from PIL import Image, ImageDraw, ImageFont
from voteConverter import convert
from booksonaGen import make_book


#fonts
arial = ImageFont.truetype('./resources/arial.ttf',20)
bigArial =  ImageFont.truetype('./resources/arial.ttf',30)
smallArial = ImageFont.truetype('./resources/arial.ttf',13)



def parse_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('input')
	parser.add_argument("-e", "--perc_elim", nargs='?', const=5, default=5)
	parser.add_argument("-t", "--num_gold", nargs='?', const=5, default=5)
	args = parser.parse_args()
	path = args.input
	
	convert(path)
	prompt = open('./{}/prompt.txt'.format(path),'r').read().split('\n')[0]
	
	twowers = []
	responses = []
	
	with open('./{}/responses.csv'.format(path),'r') as csvfile:#read responses
		reader = csv.reader(csvfile)
		for row in reader:
			twowers.append(row[0])
			responses.append(row[1])
			
	scores = [[response,[]]for response in responses]		
	votes = json.load(open('./{}/votes.json'.format(path),'r'))
	
	indiv_twowers = list(set(twowers))#data about the data (metadata?)
	twower_count = len(indiv_twowers)
	
	top_number = int(args.num_gold) #chart coloring ranges
	elim_number=0
	if int(args.perc_elim) < 0:
		elim_number = -int(args.perc_elim)
	else:
		elim_number = round(int(args.perc_elim)*len(indiv_twowers)/100)
	
	return (path, prompt, twowers, responses, scores, votes, indiv_twowers, twower_count, top_number, elim_number)
		
def wrap_text(text,chars):
	lines = textwrap.wrap(text,chars)
	new_text='\n'.join(lines)
	return new_text
	
def draw_header(prompt, base, drawer, responses):
	prompt = wrap_text(prompt,100)
	header_height = drawer.textsize(prompt,bigArial)[1]+35
	base = Image.new('RGBA',(1368,header_height+int(67/2*len(responses))),color=(255,255,255,255))
	drawer = ImageDraw.Draw(base)
	base.paste(Image.open('./resources/header.png'),(0,header_height-40))
	drawer.text((15,0),prompt,font=bigArial, fill=(0,0,0,255))
	
	return (prompt, base, drawer, header_height)

def process_votes(votes, scores, twowers):	
	for vote in votes:#maps votes to responses
		try:
			percentage = 100
			for resp_num in vote:
				scores[resp_num][1].append(percentage)
				percentage -= 11
		except Exception:
			pass

	for scoredata in scores:#calculate stats, dm if you want more
		try:
			scoredata.append(statistics.mean(scoredata[1]))	
		except Exception:
			print('{} was not voted for'.format(scoredata[0]))
			continue
			
		try:
			scoredata.append(statistics.stdev(scoredata[1]))
		except Exception:
			scoredata.append(0)
			
		scoredata.append(len(scoredata[1]))#number of votes
		scoredata[1]= twowers[scores.index(scoredata)]#twower name
		scoredata[0],scoredata[1]=scoredata[1],scoredata[0]#rearranges list in order on chart
		
	mergeSort(scores)#sorts from best to worst. Mergesort for best worst case
	return scores
	
def draw_rankings(scores, top_number, elim_number,twower_count,base,drawer,header_height,indiv_twowers):#this one is a bit of a mess
	backgroundCol=0
	addBackground=0
	ranking=1
	
	for i in range(len(scores)):	
		twower, response, mean, standev, voteCount = scores[i][0], scores[i][1], scores[i][2], scores[i][3], scores[i][4]
		
		if ranking == (top_number+1):#change background depending on ranking
			backgroundCol = 1
			addBackground = 0
		elif ranking == (twower_count-elim_number+1) and twower in indiv_twowers:
			backgroundCol = 2
			addBackground = 0
			
		if (addBackground % 2) ==0:#only needs extra stuff added every two twowers
			if backgroundCol==0:
				base.paste(Image.open('./resources/top.png'),(0,int(67/2*i)+header_height))
			elif backgroundCol==1:
				base.paste(Image.open('./resources/normal.png'),(0,int(67/2*i)+header_height))
			elif backgroundCol==2:
				base.paste(Image.open('./resources/eliminated.png'),(0,int(67/2*i)+header_height))
		
		if not os.path.isfile('./booksonas/'+twower+'.png'):
			make_book(twower,'./booksonas/')
		
		try:#attempt to add booksona
			booksona = Image.open('./booksonas/'+twower+'.png')
			booksona.thumbnail((32,32),Image.BICUBIC)
			base.paste(booksona,(333,int(67/2*i)+header_height),booksona)
		except:
			pass
			
			
		
		if twower in indiv_twowers:#handles multiple submissions
			indiv_twowers.remove(twower)
			if ranking % 10 == 1:
				rankingString = str(ranking)+'st'
			elif ranking % 10 == 2:
				rankingString = str(ranking)+'nd'
			elif ranking % 10 == 3:
				rankingString = str(ranking)+'rd'
			else:
				rankingString = str(ranking)+'th'
				
			drawer.text((15,int(67/2*i+7)+header_height),rankingString,font=arial,fill=(0,0,0,255))
			ranking += 1
			
		if drawer.textsize(twower,arial)[0] > 255: #draws twower name
			drawer.text((320-drawer.textsize(twower,smallArial)[0],int(67/2*i+7)+header_height),
				twower,font=smallArial,fill=(0,0,0,255))
				
		else:
			drawer.text((320-drawer.textsize(twower,arial)[0],int(67/2*i+7)+header_height),
				twower,font=arial,fill=(0,0,0,255))
				
		if drawer.textsize(response,arial)[0] > 618: #draws responses
			responseLines = textwrap.wrap(response,90)
			response = ''
			for s in responseLines:
				response += (s+'\n')
				
			drawer.text((378,int(67/2*i)+header_height),
				response,font=smallArial,fill=(0,0,0,255))
		else:
			drawer.text((378,int(67/2*i+7)+header_height),
				response,font=arial,fill=(0,0,0,255))
		
		#draws data
		drawer.text((998,int(67/2*i+7)+header_height),
			str(mean)[:5]+'%',font=arial,fill=(0,0,0,255))
			
		drawer.text((1164,int(67/2*i+7)+header_height),
			str(standev)[:5]+'%',font=arial,fill=(0,0,0,255))
			
		drawer.text((1309-drawer.textsize(str(voteCount),arial)[0]/2,
			int(67/2*i+7)+header_height),str(voteCount),
			font=arial,fill=(0,0,0,255))
				
		addBackground += 1
		
	return base
		
def mergeSort(alist):
    if len(alist)>1:
        mid = len(alist)//2
        lefthalf = alist[:mid]
        righthalf = alist[mid:]

        mergeSort(lefthalf)
        mergeSort(righthalf)

        i=0
        j=0
        k=0
        while i < len(lefthalf) and j < len(righthalf):
            if lefthalf[i][2] > righthalf[j][2]:
                alist[k]=lefthalf[i]
                i=i+1
            else:
                alist[k]=righthalf[j]
                j=j+1
            k=k+1

        while i < len(lefthalf):
            alist[k]=lefthalf[i]
            i=i+1
            k=k+1

        while j < len(righthalf):
            alist[k]=righthalf[j]
            j=j+1
            k=k+1
	
def main():
	path, prompt, twowers, responses, scores, votes, indiv_twowers, twower_count, top_number, elim_number = parse_args()
	
	
	base = Image.new('RGBA',(1368,1368),color=(255,255,255))
	drawer = ImageDraw.Draw(base)

	
	prompt, base, drawer, header_height = draw_header(prompt, base, drawer, responses)
	scores = process_votes(votes, scores, twowers)
	draw_rankings(scores,top_number,elim_number,twower_count,base,drawer,header_height,indiv_twowers)
	
	base.save('./'+path+'/results.png')


if __name__=='__main__':
	main()
