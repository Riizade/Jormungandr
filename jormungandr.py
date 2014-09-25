import generate
import pprint

human_data = generate.load_json("genfiles/human.json")
human = generate.generate_entity(human_data)

pprint.pprint(human)