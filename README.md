# Keeper2022_Python_Blockchain
키퍼 겨울방학 기술문서: 파이썬으로 만드는 블록체인

1. http://localhost:5000/  
블록체인 확인  
![image](https://user-images.githubusercontent.com/68144657/155150353-19e4f72e-135f-498a-a1bc-bbbf27877f20.png)

2. http://localhost:5000/mine  
채굴  
    {
        "private_key" : "1EqApkWCawAdsj2F2pkmEKrqJpQmXfGztp"
    }  
![image](https://user-images.githubusercontent.com/68144657/155150828-5465f6f4-23a7-4257-9d1d-178061130d49.png)

3. http://localhost:5000/add_transaction  
트랜잭션 추가  
보내려는 개수, 수신자, 송신자, 송신자 개인키  
    {
        "amount"     : 15,
        "receiver"   : "1HXHfqXviDK9Z9V7MBgcWdfy2tADwDFMAx",
        "sender"     : "1EqApkWCawAdsj2F2pkmEKrqJpQmXfGztp",
        "senderPrivate" : "cd0aa9856147b6c5b4ff2b7dfee5da20aa38253099ef1b4a64aced233c9afe29"
    }  
![image](https://user-images.githubusercontent.com/68144657/155151125-f8e3ee6d-e67c-4aaa-a9b7-88bcde74af2d.png)

4. http://localhost:5000/transactions  
트랜잭션 확인  
![image](https://user-images.githubusercontent.com/68144657/155151209-46a173fd-a647-4a2e-b5e7-2ac023df248f.png)
