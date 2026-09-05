import networkx as nx

def build_entity_graph(alerts: list) -> nx.Graph:
    graph = nx.Graph()

    for alert in alerts:
        alert_id = alert["id"]
        graph.add_node(alert_id, type="alert", data=alert)

        entities = extract_entities(alert["raw_fields"])
        for entity_type, entity_value in entities.items():
            entity_node = f"{entity_type}:{entity_value}"
            graph.add_node(entity_node, type="entity")
            graph.add_edge(alert_id, entity_node)

    return graph

def extract_entities(raw_fields: dict) -> dict:
    entities = {}
    if "username" in raw_fields:
        entities["user"] = raw_fields["username"]
    if "source_ip" in raw_fields:
        entities["ip"] = raw_fields["source_ip"]
    if "hostname" in raw_fields:
        entities["host"] = raw_fields["hostname"]
    return entities

def find_linked_alerts(graph: nx.Graph, alert_id: int) -> list:
    if alert_id not in graph:
        return []

    linked = set()
    for entity_node in graph.neighbors(alert_id):
        for connected_alert in graph.neighbors(entity_node):
            if connected_alert != alert_id and graph.nodes[connected_alert].get("type") == "alert":
                linked.add(connected_alert)

    return list(linked)
from app.services.attack_sequencer import infer_tactic, is_progressive_sequence

def detect_campaigns(alerts: list) -> list:
    graph = build_entity_graph(alerts)
    campaigns = []
    checked = set()

    for alert in alerts:
        alert_id = alert["id"]
        if alert_id in checked:
            continue

        linked = find_linked_alerts(graph, alert_id)
        if linked:
            all_ids = [alert_id] + linked
            tactics = [infer_tactic(a) for a in alerts if a["id"] in all_ids]

            if is_progressive_sequence(tactics):
                campaigns.append({
                    "alert_ids": all_ids,
                    "tactics": tactics
                })
                checked.update(all_ids)

    return campaigns