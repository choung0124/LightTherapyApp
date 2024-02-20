def InitialLightSettings(age, gender):
    InitialDecisionTree = {

    }

EmotionDict = {
    "행복": 1,
    "슬픔": -1,
    "분노": -1,
    "불안": -1,
    "기쁨": 1,
    "우울": -1,
    "놀람": 0,
    "공포": -1,
    "피곤": -1,
    "지침": -1,
    "지루": -1,
}

def DailyLightSettings(age,
gender, 
emotion,
activity,
time,
location,
):
    DailyDecisionTree = {
        "age": {
            "under_18": {
                "gender": {
                    "male": {
                        "


                    "female": {
                        
                    }
                },
            },
            "18_to_50": {
                "gender": {
                    "male": {

                    },
                    "female": {
                        
                    }
                },
            },
            "50_to_70": {
                "gender": {
                    "male": {

                    },
                    "female": {
                        
                    }
                },
            },
            "70_to_80": {
                "gender": {
                    "male": {

                    },
                    "female": {
                        
                    }
                },
            },
            "over_80": {
                "gender": {
                    "male": {

                    },
                    "female": {
                        
                    }
                },
            },

    }