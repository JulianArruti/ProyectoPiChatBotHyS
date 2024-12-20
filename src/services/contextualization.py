from typing import List

class Contextualization:
    def __init__(self, safety_rules: dict):
        self.safety_rules = safety_rules

    def check_expert_system(self, response: str) -> str:
        """
        Verifica reglas de seguridad en la respuesta
        """
        for rule, advice in self.safety_rules.items():
            if rule.lower() in response.lower():
                return f"Nota de Seguridad: {advice}"
        return ""

    def check_contextual_relevance(self, query: str, results: List[str]) -> bool:
        """
        Verifica relevancia contextual entre la pregunta y resultados
        """
        query_terms = set(query.lower().split())
        for result in results:
            result_terms = set(result.lower().split())
            if query_terms.intersection(result_terms):
                return True
        return False