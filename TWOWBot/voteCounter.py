#framework is here, modify as needed
import ast, argparse, statistics, textwrap
from PIL import Image, ImageDraw, ImageFont

def main():#this is an absolute mess
	parser = argparse.ArgumentParser()
	parser.add_argument('input')
	parser.add_argument("-e", "--perc_elim", nargs='?', const=5, default=5)
	parser.add_argument("-t", "--num_gold", nargs='?', const=5, default=5)
	args = parser.parse_args()
	
	keys = ast.literal_eval(open('./'+args.input+'/dict.txt','r').read())
	responses = open('./'+args.input+'/responses.txt','r').read().split('\n')
	entirevotes = open('./'+args.input+'/votes.txt','r').read().replace('[','').replace(']','').split('\n')
	twowers = open('./'+args.input+'/twowers.txt','r').read().split('\n')
	indivTwowers = list(set(twowers))
	twowerCount = len(indivTwowers)
	prompt = open('./'+args.input+'/prompt.txt','r').read().split('\n')[0]
	votes = []
	scores=[[response,[]]for response in responses]
	
	topNumber = int(args.num_gold)
	elimNumber = 0
	
	if int(args.perc_elim) < 0:
		elimNumber = -int(args.perc_elim)
	else:
		elimNumber = round(int(args.perc_elim)*len(indivTwowers)/100)
	
	
	
	promptList = textwrap.wrap(prompt,100)
	prompt = ''
	for s in promptList:
		prompt += (s+'\n')
	
	arial = ImageFont.truetype('./resources/arial.ttf',20)
	bigArial =  ImageFont.truetype('./resources/arial.ttf',30)
	smallArial = ImageFont.truetype('./resources/arial.ttf',13)
	
	base = Image.new('RGBA',(1368,1368),color=(255,255,255))
	drawer = ImageDraw.Draw(base)
	headerHeight = drawer.textsize(prompt,bigArial)[1]+35
	base = Image.new('RGBA',(1368,headerHeight+int(67/2*len(responses))),color=(255,255,255,255))
	drawer = ImageDraw.Draw(base)
	
	drawer.text((15,0),prompt,font=bigArial, fill=(0,0,0,255))
	base.paste(Image.open('./resources/header.png'),(0,headerHeight-40))
	
	for v in entirevotes:
		if not v=='':
			voteTup=tuple(v.split(' '))
			voteTup = (voteTup[0].upper(),voteTup[1].lower())
			votes.append(voteTup)
	
	for vote in votes:
		try:
			mapping = keys[vote[0]]
			percentage = 100
			for c in vote[1]:
				scores[mapping[ord(c)-97]][1].append(percentage)
				percentage -= 11
		except KeyError:
			print('Invalid vote'+': ['+vote[0]+' '+vote[1].upper()+']')
		except Exception:
			pass
	
	for scoredata in scores:
		try:
			scoredata.append(statistics.mean(scoredata[1]))			
		except Exception:
			continue
			
		try:
			scoredata.append(statistics.stdev(scoredata[1]))
		except Exception:
			scoredata.append(0)
			
		scoredata.append(len(scoredata[1]))
		scoredata[1]= twowers[scores.index(scoredata)]
		scoredata[0],scoredata[1]=scoredata[1],scoredata[0]
		
	mergeSort(scores)
	backgroundCol=0
	addBackground=0
	ranking=1
	
	for i in range(len(scores)):	
		twower, response, mean, standev, voteCount = scores[i][0], scores[i][1], scores[i][2], scores[i][3], scores[i][4]
		
		if ranking == (topNumber+1): 
			backgroundCol = 1
			addBackground = 0
		elif ranking == (twowerCount-elimNumber+1) and twower in indivTwowers:
			backgroundCol = 2
			addBackground = 0
			
		if (addBackground % 2) ==0:
			if backgroundCol==0:
				base.paste(Image.open('./resources/top.png'),(0,int(67/2*i)+headerHeight))
			elif backgroundCol==1:
				base.paste(Image.open('./resources/normal.png'),(0,int(67/2*i)+headerHeight))
			elif backgroundCol==2:
				base.paste(Image.open('./resources/eliminated.png'),(0,int(67/2*i)+headerHeight))
		
		try:
			booksona = Image.open('./booksonas/'+twower+'.png')
			booksona.thumbnail((32,32),Image.BICUBIC)
			base.paste(booksona,(333,int(67/2*i)+headerHeight),booksona)
		except Exception:
			pass
		
		if twower in indivTwowers:
			indivTwowers.remove(twower)
			if ranking % 10 == 1:
				rankingString = str(ranking)+'st'
			elif ranking % 10 == 2:
				rankingString = str(ranking)+'nd'
			elif ranking % 10 == 3:
				rankingString = str(ranking)+'rd'
			else:
				rankingString = str(ranking)+'th'
				
			drawer.text((15,int(67/2*i+7)+headerHeight),rankingString,font=arial,fill=(0,0,0,255))
			ranking += 1
		if drawer.textsize(twower,arial)[0] > 255:
			drawer.text((320-drawer.textsize(twower,smallArial)[0],int(67/2*i+7)+headerHeight),
				twower,font=smallArial,fill=(0,0,0,255))
		else:
			drawer.text((320-drawer.textsize(twower,arial)[0],int(67/2*i+7)+headerHeight),
				twower,font=arial,fill=(0,0,0,255))
				
		if drawer.textsize(response,arial)[0] > 618:
			responseLines = textwrap.wrap(response,90)
			response = ''
			for s in responseLines:
				response += (s+'\n')
				
			drawer.text((378,int(67/2*i)+headerHeight),
				response,font=smallArial,fill=(0,0,0,255))
		else:
			drawer.text((378,int(67/2*i+7)+headerHeight),
				response,font=arial,fill=(0,0,0,255))
				
		drawer.text((998,int(67/2*i+7)+headerHeight),
			str(mean)[:5]+'%',font=arial,fill=(0,0,0,255))
			
		drawer.text((1164,int(67/2*i+7)+headerHeight),
			str(standev)[:5]+'%',font=arial,fill=(0,0,0,255))
			
		drawer.text((1309-drawer.textsize(str(voteCount),arial)[0]/2,
			int(67/2*i+7)+headerHeight),str(voteCount),
			font=arial,fill=(0,0,0,255))
				
		addBackground += 1		
		
	base.save('./'+args.input+'/results.png')


	
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

if __name__=='__main__':
	main()
