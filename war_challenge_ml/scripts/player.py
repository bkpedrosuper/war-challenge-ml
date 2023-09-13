from scripts.objectives import (
    Objective,
    ObjectiveData,
    Conquer,
    ConquerData,
    generate_base_weights,
)
from scripts.army import Army, ArmyData, armydict
from war_challenge_computer_vision.regions.regions import Region, RegionData, Continent
from scripts.state import WorldState, RegionState
import numpy as np
import random


class Player:
    def __init__(self, army: ArmyData, my_objective: ObjectiveData) -> None:
        self.worldState = WorldState()
        self.army = army
        self.my_objective = my_objective
        self.worldState.set_default_weights(generate_base_weights(self.my_objective))
        self.iteration = self.range_random()
        # self.TerCOntdi
        # generate_base_weights(my_objective.value)

    def update(self, data):
        self.worldState.update(data[0])
        self.worldState.set_default_weights

    def range_random(self):
        pivot = 1.0
        i = 0
        while pivot > random.random():
            pivot *= 0.9
            i +=1
        return i

    def divide_and_conquer(self, data):
        self.worldState.update(data[0])
        conquer = []
        flag = 0
        Generate_weights = generate_base_weights(self.my_objective)
        Weights = list(zip(Region, Generate_weights))
        action = ''
        
        if self.iteration >0:
            # generate_base_weights(my_objective.value)
            for Search_Ally in self.worldState.getRegionState():
                # print(flag)
                # print(Search_Ally.army.tag,'',self.army.tag)
                

                if (
                    Search_Ally.army.tag == self.army.tag and Search_Ally.troops > 1
                ):  # Possivel
                    # print(Search_Ally.name)
                    Ally_power: float = 0.0
                    for search_Ally_Ally in self.worldState.getRegionState()[
                        flag
                    ].borders:  # noqa: E501
                        if search_Ally_Ally.army.tag == self.army:
                            # print("Entrou 3")
                            Ally_power += search_Ally_Ally.troops

                    for search_Enemy in self.worldState.getRegionState()[flag].borders:
                        if (search_Enemy.troops > Search_Ally.troops - 2):
                            continue

                        #print("####Enemy ", search_Enemy.name)
                        if search_Enemy.army.tag != self.army.tag:
                            # print("Entrou 4")
                            Enemy_power: float = 0.0
                            Weight_flag = 0
                            for Enemy in self.worldState.getRegionState()[
                                search_Enemy.idx
                            ].borders:  # noqa: E501
                                if Enemy.army.tag == self.army.tag:
                                    Weight_flag += 1
                                    continue
                                Enemy_power += Enemy.troops
                                Weight_flag += 1
                                # print(Enemy_power)
                            fit_value = (Ally_power + Search_Ally.troops) * 0.5 - (
                                (Enemy_power + search_Enemy.troops) * 0.5
                            ) / Weights[Weight_flag][
                                1
                            ]  # noqa: E501
                            conquer.append((Search_Ally.name, search_Enemy.name, fit_value)) # type: ignore # noqa: E501
                            #print("Enemy Power ", Enemy_power)
                flag += 1
            if len(conquer) ==0:
                print('finaliza ataque')
            else:
                best = conquer[0]
                for elemento in conquer:
                    if elemento[2] > best[2]:
                        elemento = best
                self.iteration -=1
                print(best[0] + ' ataca ' +best[1])
        else:
            self.iteration = self.range_random()
            print('finaliza ataque')


    def is_mine(self, regionState: RegionState):
        """Verifica se um território é meu"""
        answer = regionState.army.tag == self.army.tag
        return answer

    def move(self):
        """Calculo da defesa dos territórios"""
        # Buscamos territórios que são nossos aliados
        best_moviment_text = ''
        # Calculo das fortificações e dos movimentos
        if self.iteration > 0:
            moviments = []
            regionFortification = np.array([0.0 for _ in range(self.worldState.worldLen)])
            for regionPosition, regionState in enumerate(self.worldState.getRegionState()):
                if self.is_mine(regionState):
                    # print(Search_Ally.name)
                    fortification = float(regionState.troops)
                    for border in regionState.borders:  # noqa: E501
                        if self.is_mine(border):
                            # print("Entrou 3")
                            fortification += float(border.troops) / 2
                            # Criando possíveis alternativas e restrições
                            if regionState.troops > 1:
                                moviments.append(
                                    (regionState, border, (1, regionState.troops - 1))
                                )

                        else:
                            fortification -= border.troops
                    regionFortification[regionPosition] += fortification

            best_moviments = [
                self.fit(movement[0], movement[1], movement[2], regionFortification)
                for movement in moviments
            ]
            best_moviment = best_moviments[0]
            for movement in best_moviments:
                if movement[3] > best_moviment[3]:
                    best_moviment = movement
            best_moviment_text = best_moviment[0].name + ' -('+str(best_moviment[2]) + ')-> ' + best_moviment[1].name
            self.iteration -=1
        else:
            self.iteration = self.range_random()
            best_moviment_text = 'finaliza movimentação'

        print(best_moviment_text)

    def fit(
        self,
        stateOrigin: RegionState,
        stateDestiny: RegionState,
        troop_range: tuple[int, int],
        fortification: np.ndarray,
    ):
        best = 0
        best_troop = 0
        for troop in troop_range:
            term1 = stateOrigin.default_weight * (
                fortification[stateOrigin.idx] - troop
            )
            term2 = stateDestiny.default_weight * (
                fortification[stateDestiny.idx] + troop
            )
            fit = term1 + term2
            if fit > best:
                best = fit
                best_troop = troop

        solution = (stateOrigin, stateDestiny, best_troop, best)
        return solution


# teste
