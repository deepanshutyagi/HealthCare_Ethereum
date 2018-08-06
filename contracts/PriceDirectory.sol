pragma solidity ^0.4.18;


contract  PriceDirectoryInterface{
    
    
     // get whitelisted to offer procedures on our platform
    function applyForWhiteListing(address _provider) public returns(bool _applied);
    
    
    // Decent verifies the provider and whitelists the provider
    
    function whiteListAnyProvider(address _provider) public returns(bool _whiteListed);
                   
   //approve provider for a to list a certain procedure
    function approveProcedureListing(address _provider,uint _procedureId) public  returns(bool _procedureApproved);
    
    
    //Provider can List a procedure with a price in tokens once the procedure is approved to be listed
    
    function listProcedure(uint _procedureId,uint _priceInTokens) public returns(bool _procedureListed);
    
    //change procedure Price
    
    function changeProcedurePrice(uint _procedureId,uint _priceInTokens) public returns(bool _procedurePriceChanged);
   
    //check current procedure Price
    
    function checkCurrentProcedurePrice(address _provider,uint _procedureId) external view returns(uint _procedurePrice);
    
    //view all the procedures offered by a provider
    
    function viewProcedures(address _provider) external view returns(uint[]);
    
    //check past prices of procedure based on blockNumber
    
    function checkProcedurePriceByBlock(address _provider,uint _blocknumber,uint _procedureId) external view returns(uint _procedurePriceAtBlokcnumber);
    
    
    //check if the provider is on platform
    
    function checkIfProviderExists(address _provider) external view returns(bool);
    
    //checkALl the providers on the platform
    
    function viewAllProviders() external view returns(address[]);
    
     //Events
    
    event appliedForWhitelisting(address indexed _provider);
    event whiteListed(address indexed _provider);
    event procedureListedSuccess(address indexed _provider,uint indexed _procedureId);
    event procedureApproved (address indexed _provider,uint indexed _procedureId);
    event procedurePriceChanged(address indexed _provider,uint indexed _procedureId,uint indexed _priceChangedTo);
    
    
}


contract PriceDirectory is PriceDirectoryInterface{
    
    
    address public contractOwner;
    address[] public providers;


    
    //struct Directory to store all the price and procedure  data for health care provider
    struct directory{
        
        uint[]  procedureId;
      
        mapping(uint=>uint) procedureCurrentPrice;
        
        mapping(uint=>mapping(uint=>uint)) procedurePriceAtBlock;
        
    }
    
    
    
    //mappings
    
    // To check whether the health provider was verified before he is allowed to list his services
    mapping(address=>bool) verified;
    
    //access provider data
    mapping(address=>directory) providerData;
    
    //provider applies for whitelisting
    mapping(address=>bool) applied;
    
    //Procedure procedureListed
    
    mapping(address=>mapping(uint=>bool)) procedureListed;
    
    
    //procedureExists and approved by decent or third party
    mapping(address=>mapping(uint=>bool)) procedureExists;
    
    
    
    function PriceDirectory(){
        contractOwner=msg.sender;
        
    }
    
     //modifier
     //modifier
    modifier onlyContractOwner() {
        require(msg.sender ==contractOwner);
        _;
    }
    
    
    // get whitelisted to offer procedures on our platform
    function applyForWhiteListing(address _provider) public returns(bool _applied){
               require(verified[_provider]==false);
               require(applied[_provider]==false);
               applied[_provider]=true;
               emit appliedForWhitelisting(_provider);
               return true;
               
    }
    
    
    // Decent verifies the provider and whitelists the provider
    
    function whiteListAnyProvider(address _provider) public onlyContractOwner returns(bool _whiteListed){
                    require(verified[_provider]==false);
                    require(applied[_provider]==true);
                    verified[_provider]=true;
                    providers.push(_provider);
                    emit whiteListed(msg.sender);
                    return true;
                        
    }
    
    
    //approve provider for a to list a certain procedure
    function approveProcedureListing(address _provider,uint _procedureId) public onlyContractOwner returns(bool _procedureApproved){
                require(verified[_provider]==true);
                require(procedureListed[_provider][_procedureId]==false);
                require(procedureExists[_provider][_procedureId]==false);
                procedureExists[_provider][_procedureId]=true;
                procedureApproved(_provider,_procedureId);
                return true;
    }
    
    
    
    
    
    //Provider can List a procedure with a price in tokens once the procedure is approved to be listed
    
    function listProcedure(uint _procedureId,uint _priceInTokens) public returns(bool _procedureListed){
                        require(verified[msg.sender]==true);
                        require(procedureListed[msg.sender][_procedureId]==false);
                        require(procedureExists[msg.sender][_procedureId]==true);
                        providerData[msg.sender].procedureId.push(_procedureId);
                        providerData[msg.sender].procedureCurrentPrice[_procedureId]=_priceInTokens;
                        providerData[msg.sender].procedurePriceAtBlock[_procedureId][block.number]=_priceInTokens;
                        procedureListed[msg.sender][_procedureId]=true;
                        return true;
                        

    }
    
    //change procedure Price
    
    function changeProcedurePrice(uint _procedureId,uint _priceInTokens) public returns(bool _procedurePriceChanged){
                        require(verified[msg.sender]==true);
                        require(procedureListed[msg.sender][_procedureId]==true);
                        require(procedureExists[msg.sender][_procedureId]==true);
                        providerData[msg.sender].procedureCurrentPrice[_procedureId]=_priceInTokens;
                        providerData[msg.sender].procedurePriceAtBlock[_procedureId][block.number]=_priceInTokens;
                        emit procedurePriceChanged(msg.sender,_procedureId,_priceInTokens);
                        return true;

                        
    }
    
    //check current procedure Price
    
    function checkCurrentProcedurePrice(address _provider,uint _procedureId) external view returns(uint _procedurePrice){
                    require(verified[_provider]==true);
                    require(procedureListed[_provider][_procedureId]==true);
                    return  providerData[_provider].procedureCurrentPrice[_procedureId];
    }
    
    //view all the procedures offered by a provider
    function viewProcedures(address _provider) external view returns(uint[]){
                        require(verified[_provider]==true);
                        return providerData[_provider].procedureId;
        
        
        
    }
    
    //check past prices of procedure based on blockNumber
    
    function checkProcedurePriceByBlock(address _provider,uint _blocknumber,uint _procedureId) external view returns(uint _procedurePriceAtBlokcnumber){
                            require(verified[_provider]==true);
                            require(procedureListed[msg.sender][_procedureId]==true);
                            return  providerData[msg.sender].procedurePriceAtBlock[_procedureId][_blocknumber];

    }
    
    //check if the provider is on platform
    
    function checkIfProviderExists(address _provider) external view returns(bool){
                     require(verified[_provider]==true);
                     require(applied[_provider]==true);
                     return true;
        
    } 
    
    //checkALl the providers on the platform
    
    function viewAllProviders() external view returns(address[]){
                return providers;
    }
    
    
    
    
    
    
    
    
    
    
    
    
    
    

}