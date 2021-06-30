def convert_name(x) :
    
    if  ("+" in x["Name2"]) or ("+" in x["Name3"]) or ("믹스" in x["Name2"]) or ("믹스" in x["Name3"]) or ("mix" in x["Name2"].lower()) or ("mix" in x["Name3"].lower()) or ("mongrel" in x["Name2"].lower()) or ("mongrel" in x["Name3"].lower()) or ("혼합" in x["Name2"].lower()) or ("혼합" in x["Name3"].lower()):
        y = "Mixed"
        return y
    elif ("말티" in x["Name2"]) or ("말티" in x["Name3"]) or ("maltese" in x["Name2"].lower()) or ("maltese" in x["Name3"].lower()):
        y= "Maltese"
        return y
    elif ("푸들" in x["Name2"]) or ("푸들" in x["Name3"]) or ("poodle" in x["Name2"].lower()) or ("poodle" in x["Name3"].lower()):
        y = "Poodle"
        return y
    elif ("포메" in x["Name2"]) or ("포메" in x["Name3"]) or ("pomeranian" in x["Name2"].lower()) or ("pomeranian" in x["Name3"].lower()):
        y = "Pomeranian"
        return y
    elif ("시츄" in x["Name2"]) or ("시츄" in x["Name3"]) or ("시추" in x["Name2"]) or ("시추" in x["Name3"])or ("shih tzu" in x["Name2"].lower()) or ("shih tzu" in x["Name3"].lower()):
        y = "Shih Tzu"
        return y
    elif ("요크" in x["Name2"]) or ("요크" in x["Name3"]) or ("yorkshire" in x["Name2"].lower()) or ("yorkshire" in x["Name3"].lower()):
        y = "Yorkshire Terrier"
        return y
    elif ("치와와" in x["Name2"]) or ("치와와" in x["Name3"]) or ("chihuahua" in x["Name2"].lower()) or ("chihuahua" in x["Name3"].lower()):
        y = "Chihuahua"
        return y
    elif ("코커" in x["Name2"]) or ("코커" in x["Name3"]) or ("cocker" in x["Name2"].lower()) or ("cocker" in x["Name3"].lower()):
        y = "Cocker Spaniel"
        return y
    elif ("미니어처 핀셔" in x["Name2"]) or ("미니어처 핀셔" in x["Name3"]) or ("miniature pinscher" in x["Name2"].lower()) or ("miniature pinscher" in x["Name3"].lower()):
        y = "Miniature Pinscher"
        return y
    elif ("미니어처 슈나" in x["Name2"]) or ("미니어처 슈나" in x["Name3"]) or ("miniature schnauzer" in x["Name2"].lower()) or ("miniature schnauzer" in x["Name3"].lower()):
        y = "Miniature Schnauzer"
        return y
    elif ("비숑" in x["Name2"]) or ("비숑" in x["Name3"]) or ("bichon" in x["Name2"].lower()) or ("bichon" in x["Name3"].lower()):
        y = "Bichon Frise"
        return y
    elif ("페키" in x["Name2"]) or ("페키" in x["Name3"]) or ("pekingese" in x["Name2"].lower()) or ("pekingese" in x["Name3"].lower()):
        y = "Pekingese"
        return y
    elif ("닥스" in x["Name2"]) or ("닥스" in x["Name3"]) or ("dachshund" in x["Name2"].lower()) or ("dachshund" in x["Name3"].lower()):
        y = "Dachshund"
        return y
    elif ("스피츠" in x["Name2"]) or ("스피츠" in x["Name3"]) or ("spitz" in x["Name2"].lower()) or ("spitz" in x["Name3"].lower()):
        y = "Spitz"
        return y
    elif ("골든" in x["Name2"]) or ("골든" in x["Name3"]) or ("golden" in x["Name2"].lower()) or ("golden" in x["Name3"].lower()):
        y = "Golden Retriever"
        return y
    elif ("진도" in x["Name2"]) or ("진도" in x["Name3"]) or ("jindo" in x["Name2"].lower()) or ("jindo" in x["Name3"].lower()):
        y = "Jindo Dog"
        return y
    elif ("비글" in x["Name2"]) or ("비글" in x["Name3"]) or ("beagle" in x["Name2"].lower()) or ("beagle" in x["Name3"].lower()):
        y = "Beagle"
        return y
    elif ("코기" in x["Name2"]) or ("코기" in x["Name3"]) or ("corgi" in x["Name2"].lower()) or ("corgi" in x["Name3"].lower()):
        y = "Welsh Corgi"
        return y
    elif ("프렌치 불도그" in x["Name2"]) or ("프렌치 불도그" in x["Name3"]) or ("french bulldog" in x["Name2"].lower()) or ("french bulldog" in x["Name3"].lower()):
        y = "French Bulldog"
        return y
    elif ("보스턴" in x["Name2"]) or ("보스턴" in x["Name3"]) or ("boston" in x["Name2"].lower()) or ("boston" in x["Name3"].lower()):
        y = "Boston Terrier"
        return y
    elif ("허스키" in x["Name2"]) or ("허스키" in x["Name3"]) or ("husky" in x["Name2"].lower()) or ("husky" in x["Name3"].lower()):
        y = "Siberian Husky"
        return y
    elif ("말라" in x["Name2"]) or ("말라" in x["Name3"]) or ("mahle" in x["Name2"].lower()) or ("mahle" in x["Name3"].lower()):
        y = "Mahlemut"
        return y
    elif ("피레네" in x["Name2"]) or ("피레네" in x["Name3"]) or ("pyrenees" in x["Name2"].lower()) or ("pyrenees" in x["Name3"].lower()):
        y = "Great Pyrenees"
        return y
    else:
        y = "해당 사항 X"
        return y

def weight_category(x):
    lb = 0.454
    if x < 20 * lb:
        y = "Small"
    elif x < 50 * lb:
        y = "Medium"
    elif x < 90 * lb:
        y = "Large"
    else:
        y = "Giant"
    return y

def age_group(x):
    if x["Weight Category"]== "Small":
        if x["Month"] <= 24:
            group = "Puppy"
        elif x["Month"] <= 84:
            group = "Adult"
        elif x["Month"] <= 144:
            group = "Senior"
        else:
            group = "Geriatric"
    elif x["Weight Category"]=="Medium":
        if x["Month"] <= 12:
            group = "Puppy"
        elif x["Month"] <= 84:
            group = "Adult"
        elif x["Month"] <= 120:
            group = "Senior"
        else:
            group = "Geriatric"
    elif x["Weight Category"]=="Large":
        if x["Month"] <= 12:
            group = "Puppy"
        elif x["Month"] <= 48:
            group = "Adult"
        elif x["Month"] <= 96:
            group = "Senior"
        else:
            group = "Geriatric"
    else:
        if x["Month"] <= 12:
            group = "Puppy"
        elif x["Month"] <= 48:
            group = "Adult"
        elif x["Month"] <= 96:
            group = "Senior"
        else:
            group = "Geriatric"            
    return group

def age(x):
    # if x["Month"]==0 :
    #     y = '1개월'
    #     return y
    # elif x["Month"]==1 :
    #     y = '2개월'
    #     return y
    # elif x["Month"]==2 :
    #     y = '3개월'
    #     return y
    # elif x["Month"]==3 :
    #     y = '4개월'
    #     return y
    # elif x["Month"]==4 :
    #     y = '5개월'
    #     return y
    # elif x["Month"]==5 :
    #     y = '6개월'
    #     return y
    # elif x["Month"]==6 :
    #     y = '7개월'
    #     return y
    # elif x["Month"]==7 :
    #     y = '8개월'
    #     return y
    # elif x["Month"]==8 :
    #     y = '9개월'
    #     return y
    # elif x["Month"]==9 :
    #     y = '10개월'
    #     return y
    # elif x["Month"]==10 :
    #     y = '11개월'
    #     return y
    # elif x["Month"]==11 :
    #     y = '12개월'
    #     return y
    if (x["Month"]>=0) & (x["Month"]<=11) :
        y = 'Puppy'
        return y
    elif (x["Month"]>11) & (x["Month"]<=23) :
        y = '2살'
        return y
    elif (x["Month"]>23) & (x["Month"]<=35) :
        y = '3살'
        return y
    elif (x["Month"]>35) & (x["Month"]<=47) :
        y = '4살'
        return y
    elif (x["Month"]>47) & (x["Month"]<=59) :
        y = '5살'
        return y
    elif (x["Month"]>59) & (x["Month"]<=71) :
        y = '6살'
        return y
    elif (x["Month"]>71) & (x["Month"]<=83) :
        y = '7살'
        return y
    elif (x["Month"]>83) & (x["Month"]<=95) :
        y = '8살'
        return y
    elif (x["Month"]>95) & (x["Month"]<=107) :
        y = '9살'
        return y
    elif (x["Month"]>107) & (x["Month"]<=119) :
        y = '10살'
        return y
    elif (x["Month"]>119) & (x["Month"]<=131) :
        y = '11살'
        return y
    elif (x["Month"]>131) & (x["Month"]<=143) :
        y = '12살'
        return y
    elif (x["Month"]>143) & (x["Month"]<=155) :
        y = '13살'
        return y
    elif (x["Month"]>155) & (x["Month"]<=167) :
        y = '14살'
        return y
    elif (x["Month"]>167) & (x["Month"]<=179) :
        y = '15살'
        return y
    elif (x["Month"]>179) & (x["Month"]<=191) :
        y = '16살'
        return y
    elif (x["Month"]>191) & (x["Month"]<=203) :
        y = '17살'
        return y
    elif (x["Month"]>203) & (x["Month"]<=215) :
        y = '18살'
        return y
    elif (x["Month"]>215) & (x["Month"]<=227) :
        y = '19살'
        return y
    elif (x["Month"]>227) & (x["Month"]<=239) :
        y = '20살'
        return y
    else:
        y = '20살이상'
        return y