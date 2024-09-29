import json
import translate_file_to_eng

accident_file_base = "bf_ids.json"
accident_file = "bf_ids_eng.json"

def coords_match(crash_point, point1, point2, accuracy=0.0009):#about 100m accuracy
    extrema_x = {}
    extrema_y = {}
    extrema_x[0] = min(point1[0], point2[0])
    extrema_x[1] = max(point1[0], point2[0])
    extrema_y[0] = min(point1[1], point2[1])
    extrema_y[1] = max(point1[1], point2[1])

    if extrema_x[0] - accuracy > crash_point[0] or extrema_x[1] + accuracy < crash_point[0]:
        return False

    if extrema_y[0] - accuracy > crash_point[1] or extrema_y[1] + accuracy < crash_point[1]:
        return False

    return True


def get_route_accidents(route):
    global accident_file, accident_file_base

    translate_file_to_eng.translate_file(accident_file_base, accident_file)
    accidents = {}

    with open(accident_file, 'r') as f:
        data = json.load(f)
        for key_crashes, value_crashes in data.items():
            crash_vals = {}
            crash_vals[0] = value_crashes['gps_y']
            crash_vals[1] = value_crashes['gps_x']
            for i in range(len(route) - 1):
                point1 = route[i]
                point2 = route[i + 1]
                if coords_match(crash_vals, point1, point2):
                    print(f"1: {point1}")
                    print(f"2: {point2}")
                    print(f"crash: {crash_vals}")

                    accidents[key_crashes] = value_crashes
    return accidents

def score_accident(route):
    multiplier = 1.0
    accidents = get_route_accidents(route)
    for _, accident in accidents.items():
        for participant in accident['participants'].values():
            for victim_type, victim_data in participant['victims'].items():
                for injury in victim_data['injuries']:
                    if injury == 'No injuries':
                        multiplier += 0.3
                    elif injury == 'Minor':
                        multiplier += 1
                    elif injury == 'Severe':
                        multiplier += 4
                    elif injury == 'Dead on spot of accident':
                        multiplier += 7
    return multiplier










if __name__ == '__main__':
    dummy_route = [
	[
		50.0634159,
		19.9329681
	],
	[
		50.0632718,
		19.9328029
	],
	[
		50.0626276,
		19.9320892
	],
	[
		50.0620745,
		19.9335343
	],
	[
		50.062038,
		19.933625
	],
	[
		50.0617709,
		19.9342894
	],
	[
		50.062523,
		19.9349872
	],
	[
		50.0632688,
		19.9357144
	],
	[
		50.0633444,
		19.9355881
	],
	[
		50.0639207,
		19.936112
	],
	[
		50.0639732,
		19.9361602
	],
	[
		50.0642714,
		19.9351947
	],
	[
		50.0647684,
		19.9366835
	],
	[
		50.0648199,
		19.9368303
	],
	[
		50.0648458,
		19.936904
	],
	[
		50.0653868,
		19.9371071
	],
	[
		50.0653243,
		19.9387072
	],
	[
		50.0647665,
		19.9397421
	],
	[
		50.0642,
		19.9393552
	],
	[
		50.063982,
		19.9391896
	],
	[
		50.063656,
		19.938951
	],
	[
		50.0631804,
		19.9386136
	],
	[
		50.0631412,
		19.9385853
	],
	[
		50.0624762,
		19.9410176
	],
	[
		50.0616829,
		19.940424
	],
	[
		50.0612771,
		19.9418132
	],
	[
		50.0613505,
		19.9432247
	],
	[
		50.0611665,
		19.9441134
	],
	[
		50.062778,
		19.9449678
	],
	[
		50.0633876,
		19.9450642
	]
]
    result = get_route_accidents(dummy_route)
    score = score_accident(dummy_route)
    #print(f"result 1:{result}")
    print(f"result 1 score:{score}")

    dummy_route2 = [
	[
		50.0632718,
		19.9328029
	],
	[
		51.1181104,
		20.2761937
	],
	[
		50.0626276,
		19.9320892
	],
	[
		50.0620745,
		19.9335343
	],
	[
		50.062038,
		19.933625
	],
	[
		50.0617709,
		19.9342894
	],
	[
		50.062523,
		19.9349872
	],
	[
		50.0632688,
		19.9357144
	],
	[
		50.0633444,
		19.9355881
	],
	[
		50.0639207,
		19.936112
	],
	[
		50.0639732,
		19.9361602
	],
	[
		50.0642714,
		19.9351947
	],
	[
		50.0647684,
		19.9366835
	],
	[
		50.0648199,
		19.9368303
	],
	[
		50.0648458,
		19.936904
	],
	[
		50.0653868,
		19.9371071
	],
	[
		50.0653243,
		19.9387072
	],
	[
		50.0647665,
		19.9397421
	],
	[
		50.0642,
		19.9393552
	],
	[
		50.063982,
		19.9391896
	],
	[
		50.063656,
		19.938951
	],
	[
		50.0631804,
		19.9386136
	],
	[
		50.0631412,
		19.9385853
	],
	[
		50.0624762,
		19.9410176
	],
	[
		50.0616829,
		19.940424
	],
	[
		50.0612771,
		19.9418132
	],
	[
		50.0613505,
		19.9432247
	],
	[
		50.0611665,
		19.9441134
	],
	[
		50.062778,
		19.9449678
	],
	[
		50.0633876,
		19.9450642
	]
]
    result2 = get_route_accidents(dummy_route2)
    score2 = score_accident(dummy_route2)
    #print(f"result 2:{result2}")
    print(f"result 2 score:{score2}")

    dummy_route3 = [(50.0600246, 19.9715055), (50.0598741, 19.9722713), (50.0593773, 19.9750134), (50.0593656, 19.9756849), (50.0593925, 19.9756943), (50.0596807, 19.9757852), (50.0598101, 19.9757556), (50.0598533, 19.9759545), (50.0600113, 19.9768042), (50.0610334, 19.9792379), (50.0611225, 19.9794458), (50.0616589, 19.9805467), (50.0619815, 19.9813726), (50.0625419, 19.9825387), (50.0633178, 19.9841272), (50.0642784, 19.9877577), (50.0642967, 19.9878469), (50.0643181, 19.9879519), (50.0644959, 19.988852), (50.0645139, 19.9889433), (50.0645604, 19.9890254), (50.0645891, 19.9892045), (50.0646214, 19.9894068), (50.0646483, 19.9895633), (50.0646478, 19.9897204), (50.0647771, 19.9908134), (50.065221, 19.9934197), (50.0653111, 19.9939309), (50.0657553, 19.9965483), (50.065785, 19.9967383), (50.0658088, 19.9968747), (50.0658369, 19.9970461), (50.0672685, 20.0036855), (50.0674006, 20.0038554), (50.0676441, 20.0039153), (50.0680682, 20.0040289), (50.0699899, 20.004351), (50.070154, 20.0034494), (50.0702836, 20.0027453), (50.0698326, 20.0027528), (50.0697637, 20.0027219), (50.0691646, 20.0024815), (50.0694383, 20.0007742), (50.069576, 20.0000052), (50.0695415, 19.9993989)]
    result3 = get_route_accidents(dummy_route3)
    score3 = score_accident(dummy_route3)
    #print(f"result 2:{result2}")
    print(f"result 3 score:{score3}")
