Introduction = "<s> [INST] Below is some dialogue spoken by a person in a conversation."

AgePrompt = """{Introduction}
Please extract the age of the person speaking in the dialogue.
When presenting the extracted age, strictly use the following format:
{{
    "age": <age>
}}
If the age is not mentioned in the dialogue, please present the following:
{{
    "age": None
}}
Dialogue:
{Dialogue} [/INST]"""

ExtractionPropmt = """<s> [INST] Below is an article related to light therapy
Please extract the entities and the relations between them.
Here are the entity types:
- Treatment
- Symptom
- Disease
- Drug
- SideEffect
- Procedure
- Test
- Anatomy
- Route
- Frequency
- Duration
- Severity
Here are the Entities:
{entities}
Here are the Relations:
- Treats
- Causes
- Prevents
- Diagnoses
- Tests
- Affects
- Indicates
- Involves
- Upregulates
- Downregulates
- AssociatedWith
When presenting the extracted entities and relations, please use the following format
{{
    "entities": [
        {{
            "entityType": <entityType>,
            "entity": <entity>
        }},
        ...
    ],
    "relations": [
        {{
            "relation": <relation>,
            "entity1": <entity1>,
            "entity2": <entity2>
        }},
        ...
    ]
}}
if there are no entities or relations, please present the following:
{{
    "entities": [],
    "relations": []
}}
Article:
{Article} [/INST]"""

GenderPrompt = """{Introduction}
Please extract the gender of the person speaking in the dialogue.
When presenting the extracted gender, strictly use the following format:
{{
    "gender": <gender>
}}
If the gender is not mentioned in the dialogue, please present the following:
{{
    "gender": None
}}
Dialogue:
{Dialogue} [/INST]"""

Introduction = "<s> [INST] 아래는 대화에서 한 사람이 말한 대사입니다."

AgePrompt = """{Introduction}
대화에서 말하는 사람의 나이를 추출해주세요.
추출한 나이를 제시할 때, 반드시 다음 형식을 사용해주세요:
{{
    "age": <age>
}}
대화에서 나이가 언급되지 않은 경우, 다음을 제시해주세요:
{{
    "age": None
}}
대화:
{Dialogue} [/INST]"""

GenderPrompt = """{Introduction}
대화에서 말하는 사람의 성별을 추출해주세요.
추출한 성별을 제시할 때, 반드시 다음 형식을 사용해주세요:
{{
    "gender": <gender>
}}
대화에서 성별이 언급되지 않은 경우, 다음을 제시해주세요:
{{
    "gender": None
}}
대화:
{Dialogue} [/INST]"""


