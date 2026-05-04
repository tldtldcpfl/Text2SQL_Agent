# AGrail: A Lifelong Agent Guardrail with Effective and Adaptive Safety Detection

## Challenges of existing approaches
- 운영 체제 제어와 연동된 Agent의 경우 접근 제한된 데이터에 overwirte할 수 있기 때문에, 이러한 데이터 오염 문제를 제어할 수 있는 접근 제어 방법론이 필요하다.
- 여기서 중요한 점은 다중 Agent 시스템의 각 task마다 **risk 요소를 adaptive하게 식별**해야하는 점이다. 같은 데이터라도 task가 달라지면 접근 제한/허용 여부가 달라져야한다. 정규 표현식으로 수동으로 변수를 정의하는 방식은 광범위한 데이터 거버넌스와 스키마를 일반화하여 제어하기에는 한계가 있다.

## Adaptive Safety Check Generation
- 이 프레임워크에서는 risk 탐지 프로세스를 통해 safety verfication item을 참조하여 safety check하는 방식을 제안한다. 프레임워크의 성능을 평가하기 위해 사용된 벤치마크 데이터셋은 [Mind2Web-SC](https://huggingface.co/datasets/osunlp/Online-Mind2Web/viewer/default/test?row=0)이며, 이 데이터셋은 다음과 같은 컬럼으로 구성된다: task id, confirmed task (task name), web site, level.   


## References
- https://aclanthology.org/2025.acl-long.399.pdf
