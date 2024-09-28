
import requests
import time
import json

hits = 0

def query_api(start_id, range_width, cluster_nb, delay=0.3, time_limit=1200):#20 min max
    start_time = time.time()
    url = 'https://obserwatoriumbrd.pl/app/api/nodes/post_zdarzenie.php'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': 'pll_language=en'
    }
    
    valid_ids = {}
    global hits
    next_jump = 1
    cur_id = start_id
    #mem_max_valid = start_id
    exponential = 1.0
    while cur_id < start_id + range_width:
        if time.time() - start_time > time_limit:
            print(f"time limit reached for cluster {start_id + range_width // 2}")
        data = {'zdarzenie_id': cur_id}
        try:
            response = requests.post(url, headers=headers, data=data)
            response_data = response.json()
            if response_data.get("wsp_gps_x") is not None:
                print(f"valid ID {cur_id}: {response.text[:200]}...")
                valid_ids[cur_id] = response_data
                #backtrack on hits to check for local clustering
                #mem_max_valid = cur_id
                cur_id = cur_id - next_jump + 1
                print("backtracking..")
                next_jump = 1
                exponential = 1.0
                hits = hits + 1
            else:
                exponential = exponential * 1.005
                next_jump = int((next_jump * exponential + 1) // 1)
                print(f"invalid ID {cur_id}: {response.text[:200]}...")
        except json.JSONDecodeError:
            print(f"error decoding JSON from response for ID {cur_id}")
        except Exception as e:
            print(f"error: {e}")
        cur_id = cur_id + next_jump
        print(f"cluster {cluster_nb} / 3: {(cur_id - start_id) / range_width * 100}% ({hits} total hits)")
        time.sleep(delay)
    print(f"return with cur: {cur_id}")
    return valid_ids

cluster_centers = [203244602, 212158599, 207309186]

all_valid_ids = {}

i = 1
for center in cluster_centers:
    print(f"guessing around cluster center: {center}")
    valid_ids = query_api(center, (207418802 - 207243920) * 2, i)
    i = i + 1
    #valid_ids = query_api(center, 1)
    all_valid_ids.update(valid_ids)

print("all valid IDs collected:")
print(json.dumps(all_valid_ids, indent=4))
print(f"{hits} total hits")
with open('bf_ids.json', 'w') as f:
    json.dump(all_valid_ids, f, indent=4)
