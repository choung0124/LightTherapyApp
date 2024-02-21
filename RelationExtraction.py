import requests
import json
is function splits text into chunks of 2000 characters, with an overlap of 200 characters

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
Here is the list of possible entities in the article:
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
When presenting the extracted entities and relations, please use the following format:
*start
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
*end
if there are no entities or relations, please present the following:
{{
    "entities": [],
    "relations": []
}}
Article:
{Article} [/INST]"""

def Inference(prompt):
    # Your API endpoint URL
    api_url = "http://192.168.100.116:5000/v1/completions"

    # Replace these with your actual header values
    headers = {
        "x-api-key": "469d6ea84d28a773fbcffdf25e9d2616",
        "Content-Type": "application/json"
        }

    # Example request body with parameters as described
    request_body = {
    "max_tokens": 2048,
    "stop": "*end",
    "token_healing": True,
    "temperature": 1,
    "temperature_last": True,
    "smoothing_factor": 0,
    "top_k": 1,
    "min_p": 0.05,
    "frequency_penalty": 0,
    "presence_penalty": 0,
    "repetition_penalty": 1,
    "repetition_decay": 0,
    "mirostat_mode": 0,
    "mirostat_tau": 1.5,
    "mirostat_eta": 0.3,
    "add_bos_token": True,
    "ban_eos_token": False,
    "logit_bias": {"1": 10},
    "typical": 1,
    "penalty_range": 0,
    "cfg_scale": 1,
    "max_temp": 1,
    "min_temp": 1,
    "temp_exponent": 1,
    "model": "string",
    "stream": False,
    "logprobs": 0,
    "best_of": 0,
    "echo": False,
    "n": 1,
    "suffix": "string",
    "user": "string",
    "prompt": prompt
    }

    response = requests.post(api_url, headers=headers, json=request_body)
    response_body = response.json()
    text_result = response_body['choices'][0]['text']
    print(text_result)
    ### Find "*start" and "*end" in the text_result
    start_marker = "*start"
    end_marker = "*end"
    start_pos = text_result.find(start_marker) + len(start_marker)
    end_pos = text_result.find(end_marker, start_pos)
    json_content = text_result[start_pos:end_pos].strip()

    # Step 3: Parse the JSON string
    try:
        json_data = json.loads(json_content)
        return json_data
    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON: {e}")

article = """LED lighting. In particular, a significant number of people
spend up to 90% of their time under indoor electrical
lighting.20 This means that, during the day, we can be exposed
to bright artificial lighting with radiation energy of approximately 480 nm wavelength, which is equivalent to a sufficient
dose of actual daylight. This specific light, which is associated
with melatonin suppression and secretion, can be applied to
functional artificial lighting to regulate alertness, sleep, and the
circadian rhythm.21−23
The attention of many researchers is shifting from the
performance of lighting in terms of energy to lighting quality
that can affect human productivity, comfort, mood, safety, and
health.24 As such, many researchers and experts have thought
about lighting as “circadian lighting”, “biological lighting”, and
“human-centric lighting (HCL)”. Some studies have offered
evidence and support of a high CRI, the convenience of smart
lighting, low glaring lighting, and melatonin related lighting for
HCL.25 Furthermore, to produce a lighting effect on the
human body, there are various ways to adjust the correlatedcolor temperature (CCT) using warm-white (WW), coolwhite (CW), and near-ultraviolet (n-UV) LEDs, similar to the
sunlight spectrum.26 In this study, we developed LED packages
focused on blue light with a wavelength of 480 nm, which is
directly related to melatonin secretion and suppression, as
HCL. Because the melatonin concentration should be
maintained differently during the daytime and nighttime, our
human-centric (HC)-LEDs were developed separately for
daytime and nighttime. White HC-LED packages containing
two blue chips emitting light with a wavelength of 450 and 480
nm were implemented to have a total 12 types of CCT
depending on the application. In addition, HC-LED packages
have almost the same color coordinates as conventional LED
(c-LED) packages having the same CCT, and hence, there is
no change in perceived color. Ultimately, to verify the
nonvisual effects of the developed LED package, melatonin
level data from 22 voluntary participants were collected under
c- and HC-LED lighting environments with the same
illuminance and CCT. The melatonin concentration analysis
results indicate that the light-induced melatonin control was
more effective in the HC-LED lighting environment with a
regulated wavelength of 480 nm considering the circadian
rhythm than in the c-LED lighting environment. Therefore, the
daytime and nighttime HC-LEDs can be sufficiently used for
indoor lighting from a human point of view rather than from
an energy point of view, and HC-LEDs can help to enhance
the circadian rhythm of people today who spend most of their
time indoors.
2. EXPERIMENTAL SECTION
2.1. LED Package and Spectral Design. The LED
package design consists of two chips: (1) a chip emitting light
with a wavelength of 470 to 480 nm for melatonin suppression
and secretion control and (2) another chip emitting light with
a wavelength of 445 to 455 nm to secure the original optical
properties of a blue light emitter. The spectral designs varied
from WW with a CCT of 1800 K to CW with a CCT of 6500
K. The designed LED package was divided into two types of
LEDs according to the usage time period: (1) daytime LEDs
with a CCT of 3000 to 6500 K were designed to rapidly
suppress melatonin immediately after waking up and improve
subjective drowsiness, and (2) nighttime LEDs with a CCT of
1800 to 4000 K were designed to activate melatonin secretion
at night. For all types of LEDs, a CRI of >80 was achieved. The
characteristics of the prepared dual-blue-chip LEDs were
evaluated using an integrating sphere with a diameter of 300
mm by applying a current of 150 mA. The melanopic/
photopic (M/P) ratio, which is considered the ratio of
magnitude of nonvisual effects of the developed LED, was
compared with that of a c-LED series (LM302Z+, Samsung
Electronics, Co., Ltd., Korea) with the same package structure,
power consumption, and CCT (see Table S1). The M/P ratio
is expressed by the following equation:27
E N d
K E V d
M/Pratio 72983.25 ( ) ( )
( ) ( ) m
e, z
e,
=
(1)
where Ee,λ(λ) is the spectral irradiance, Nz(λ) is the melanopic
sensitivity curve, V(λ) is the photopic spectral luminous
efficiency function, and Km is the maximum spectral luminous
efficacy of 683.002 lm/W.
2.2. Participants. To confirm the effect on circadian
rhythm, this study was conducted with 22 Korean health male
volunteers, and there were no female participants. The average
age of the participants was 27.4 ± 4.36 years (mean ± SD).
The self-reported questionnaires, in this case, the Korean
version of the Pittsburgh Sleep Quality Index (PSQI-K)28 and
Epworth Sleepiness Scale (ESS),29 were administered to
participants 1 week prior to admission; PSQI-K was 6.4 ±
1.2 in the range of 4 to 8, and ESS was 5.7 ± 2.7 in the range of
1 to 10. In PSQI-K, the cutoff score between good and poor
sleepers was modified from 5 to 8.5 in the process of adapting
the conventional PSQI into Korean.28 Therefore, all
participants were considered to have a normal circadian
rhythm. In addition, according to the responses to the self"""

Entities = [
    {
        "entityType": "Anatomy",
        "entity": "melatonin"
    },
    {
        "entityType": "Anatomy",
        "entity": "lighting"
    },
    {
        "entityType": "Anatomy",
        "entity": "LED"
    },
    {
        "entityType": "Anatomy",
        "entity": "lighting"
    },

]

prompt = ExtractionPropmt.format(entities=Entities, Article=article)
result = Inference(prompt)
print(result)