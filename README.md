# Keeper2022_Python_Blockchain
키퍼 겨울방학 기술문서: 파이썬으로 만드는 블록체인

1. http://localhost:5000/  
블록체인 확인  
![image](https://user-images.githubusercontent.com/68144657/155157433-1e9e57dc-5cc3-414b-b34b-1475094dbcb4.png)  

2. http://localhost:5000//generatekey'  
키 발행 (코드 수정하면 다양한 키를 발행할 수 있음 - 트랜잭션 사용을 위해 결과 내용은 반드시 기록해야 함)  
![image](https://user-images.githubusercontent.com/68144657/155156189-f2a482f2-a5d6-47b2-ba8b-c84d94dbcd80.png)  
* 키 예시  
```json
    {  
        "address": "1HXHfqXviDK9Z9V7MBgcWdfy2tADwDFMAx",  
        "private_key": "de7d1b721a1e0632b7cf04edf5032c8ecffa9f9a08492152b926f1a5a7e765d7",  
        "public_key": "04bd8d4168be00ac2e680089a6e59551dc42fd3ec98a09965f877a09dc165a05f9845da1d36c6ddaf04a7f84f77dc3f2b6b8392d7b03eb579e9b5d4101425c4efa"  
    }

    {
        "address": "17ftYQ3TWG8ddGXBTbmLmm7tG3oXSy9HTo",  
        "private_key": "cd0aa9856147b6c5b4ff2b7dfee5da20aa38253099ef1b4a64aced233c9afe29",  
        "public_key": "04b546b2a1903e3912260fea264625191395cbb71a996815fdcbbec58ddcc05db522c1dbbc43ee2cd4f946b1cfccd85c8f85486ede484033fc8a023ec7fd57e6d2"  
    }  
'''
3. http://localhost:5000/mine   
채굴  
```json
    {  
        "private_key" : "1EqApkWCawAdsj2F2pkmEKrqJpQmXfGztp"  
    }  
'''
![image](https://user-images.githubusercontent.com/68144657/155157988-03799764-21fb-4278-bbe7-202be67eafa1.png)    

4. http://localhost:5000/add_transaction  
트랜잭션 추가  
보내려는 개수, 수신자, 송신자, 송신자 개인키  
```json
    {  
        "amount"     : 15,  
        "receiver"   : "1HXHfqXviDK9Z9V7MBgcWdfy2tADwDFMAx",  
        "sender"     : "1EqApkWCawAdsj2F2pkmEKrqJpQmXfGztp",  
        "senderPrivate" : "cd0aa9856147b6c5b4ff2b7dfee5da20aa38253099ef1b4a64aced233c9afe29"  
    }   
'''
![image](https://user-images.githubusercontent.com/68144657/155188478-c4a78704-c91a-42ba-892c-74ded0046792.png)


5. http://localhost:5000/transactions  
트랜잭션 확인  
![image](https://user-images.githubusercontent.com/68144657/155151209-46a173fd-a647-4a2e-b5e7-2ac023df248f.png)  

6. http://localhost:5000/transactions/connect_node  
노드 연결 (Post)
```json
{
    "nodes" : ["http://192.168.87.47:50001"]
}
```
![image](https://user-images.githubusercontent.com/68144657/155158145-3ae94c3e-83ff-4063-ad8a-4fbe77ae9236.png)  

7.http://localhost:5000/transactions/update_chain    
체인 업데이트  
![image](https://user-images.githubusercontent.com/68144657/155158276-0a582da6-d049-4798-9a63-2f9d74d03983.png)  


