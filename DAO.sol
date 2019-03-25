pragma solidity ^0.5.1;
contract simpleDAO {
    
    event PaymentCalled(address payee, uint amount);
    event TokensBought(address buyer, uint amount);
    event TokensTransfered(address from, address to, uint amount);
    event InsufficientFunds(uint bal, uint amount);
    
    mapping (address => uint) public balances;
    
    
    function buyTokens() public payable {
        balances[msg.sender] += msg.value;
        emit TokensBought(msg.sender, msg.value);
    }
    
    function transferTokens(address _to, uint _amount) public {
        require(balances[msg.sender] >= _amount);
        balances[_to] += _amount;
        balances[msg.sender] -= _amount;
        emit TokensTransfered(msg.sender, _to, _amount);
    }
    
    function withdraw(address _recipient) public returns (bool) {
        if (balances[msg.sender] == 0) {
            emit InsufficientFunds(balances[msg.sender], balances[msg.sender]);
        }    
        require(balances[msg.sender] > 0);
        emit PaymentCalled(_recipient, balances[msg.sender]);
        bool complete;    
        (complete,) = _recipient.call.value(balances[msg.sender])("");   
        if (complete) {
            balances[msg.sender] = 0;
            return true;
        }
        
    }
}