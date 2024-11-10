import os
import sys
import json

files = os.listdir("ideogram_requests")
os.makedirs("myPrompts",exist_ok=True)
myPrompts=set()
genPrompts=set()

for doPrivate in [False, True]:
    for file in files:
        if 'page' in file and file.endswith('.json'):
            if doPrivate and 'private' not in file:
                continue
            if not doPrivate and 'private' in file:
                continue
            fp=os.path.join("ideogram_requests",file)
            with open(fp,"r") as f:
                print(fp)
                data = json.load(f)
                for el in data:
                    if 'upload_type' in el and el['upload_type']=='upload':
                        continue
                    if 'upload_type' in el and el['upload_type']=='edit':
                        continue
                    if 'user_prompt' in el :
                        myPrompts.add(el['user_prompt'])
                    else:
                        import ipdb;ipdb.set_trace()
                    for rr in el['responses']:
                        genPrompts.add(rr['prompt'])


    myPrompts=set([el.replace("\n"," ").strip() for el in myPrompts])
    genPrompts=set([el.replace("\n"," ").strip() for el in genPrompts])

    # print(sorted(myPrompts))
    # print(sorted(genPrompts))
    print("all Private=%s prompts so far, %d by me and %d generated. "%(doPrivate, len(myPrompts),len(genPrompts)))

    if doPrivate:

        open(os.path.join("myPrompts","myPrompts-private.txt"),'w',encoding='utf-8').write('\n'.join(sorted(myPrompts)))
        open(os.path.join("myPrompts","myGenPrompts-private.txt"),'w',encoding='utf-8').write('\n'.join(sorted(genPrompts)))
    else:
        open(os.path.join("myPrompts","myPrompts.txt"),'w',encoding='utf-8').write('\n'.join(sorted(myPrompts)))
        open(os.path.join("myPrompts","myGenPrompts.txt"),'w',encoding='utf-8').write('\n'.join(sorted(genPrompts)))

