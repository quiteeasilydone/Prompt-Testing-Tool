import openai
import numpy as np

def ask_openai(key:str, model: str, temp: float, max_len: int, top_p: float, system: str, user: str, test_num: int, target: str) -> str:
    openai.api_key = key
    
    system_prompt = system
    similarity_list = []
    
    consistency = 0
    base_embed = None
    
    target_embed = openai.embeddings.create(
	model="text-embedding-3-small",
	input=target
		).data[0].embedding
    
    for i in range(test_num):
        response = openai.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user
                }
            ],
            max_tokens=max_len,
            temperature=temp,
            top_p=top_p
        )
        
        response = response.choices[0].message.content
        response_embed = openai.embeddings.create(
            model="text-embedding-3-small",
            input=response
                ).data[0].embedding
        
        if base_embed == None:
            base_embed = response_embed
        else:
            consistency += cos_sim(base_embed, response_embed)
        
        similarity = cos_sim(target_embed, response_embed)
        
        similarity_list.append((response, similarity))
    
    # average_sim = calculate_average_b(similarity_list)
    
    consistency = consistency / test_num
    
    max_res, min_res = find_extreme_a(similarity_list)
    
    return consistency, max_res, min_res, similarity_list

def cos_sim(a: list, b: list) -> float:
	return np.dot(a, b)/(np.linalg.norm(a)*np.linalg.norm(b))

def calculate_average_b(data):
    if not data:
        return 0  # 리스트가 비어있을 경우 평균을 0으로 반환

    # 모든 튜플의 두 번째 요소 b 값의 합계를 구하고, 데이터 개수로 나눔
    total_b = sum(b for _, b in data)
    average_b = total_b / len(data)
    return average_b

def find_extreme_a(data):
    if not data:
        return None, None  # 리스트가 비어있을 경우 None 반환

    # 초기값 설정
    min_a = max_a = data[0][0]
    min_b = max_b = data[0][1]

    # 리스트 순회하며 최댓값과 최솟값 업데이트
    for a, b in data:
        if b > max_b:
            max_b = b
            max_a = a
        elif b == max_b:
            continue  # 가장 앞의 a 값을 유지하기 위해

        if b < min_b:
            min_b = b
            min_a = a
        elif b == min_b:
            continue  # 가장 앞의 a 값을 유지하기 위해

    return (max_a, max_b), (min_a, min_b)