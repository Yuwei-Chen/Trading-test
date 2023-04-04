import json;
import random;

class Positions:
    def __init__(self, positions: dict[str, float]):
        self._pos = positions

    def get_universe(self) -> list[str]:
        '''
        Return list of stocks keys in portfolio university
        '''
        return list(self._pos.keys())
    
    def get_positions(self) -> dict[str, float]:
        '''
        The units of a stock are being held
        '''
        return self._pos

class Broker:
    def __init__(self, initial_positions: Positions, initial_aum: float):
        # Broker position and Broker asset under management
        self.positions = initial_positions
        self.aum = initial_aum

    def get_live_price(self) -> dict[str, float]:
        '''
        Return Dictionary of live stock prices
        '''
        prices = {asset: random.uniform(10, 30) for asset in \
                  self.positions.get_universe()} 
        return prices
        
    def get_positions(self) -> Positions:
        '''
        Return the Positions of portfolio
        '''
        return self.positions

    def execute_trades(self, execution_positions: Positions) -> None:
        pass

class RebalancingSystem:
    def __init__(self, target_Weights: dict[str, float], broker: Broker):
        self.tgtWeights = target_Weights
        self.broker = broker

    def target_positions(self) -> dict[str, float]:
        '''
        Return the dictionary containing target value of each stock
        '''
        target_holdings = {}
        prices = self.broker.get_live_price()
        for stock_key, stock_wgts in self.tgtWeights.items():
            target_mktvalue = self.broker.aum * stock_wgts
            target_holdings[stock_key] = target_mktvalue / prices[stock_key]
        return target_holdings

    def holding_excution(self, out_put_name: str) -> None:
        '''
        Generate JSON file of trades for target portfolio allocatio
        '''
        current_holdings = self.broker.get_positions().get_positions()
        tgt_holdings = self.target_positions()
        excutedTrades = {asset: tgt_holdings[asset] - current_holdings[asset] \
                         for asset in tgt_holdings.keys()}
        with open(out_put_name, 'w') as outfile:
            json.dump(excutedTrades, outfile)

if __name__ == '__main__':
    
    # load JSON files
    json_input_name = 'targetWeights_20230321.json'
    json_output_name = 'executedTrades_20230321.json'
    f = open(json_input_name)
    tgtweights = json.load(f)
    f.close()

    # Hardcode an initial Broker class
    test_positions = Positions({item: 0 for item in tgtweights.keys()})
    test_broker = Broker(test_positions, 10000.0)

    # Generate JSON file with execution
    test_rebalance = RebalancingSystem(tgtweights, test_broker)
    test_rebalance.holding_excution(json_output_name)