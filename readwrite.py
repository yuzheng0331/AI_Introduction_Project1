import json
import csv

class GraphIO:
    @staticmethod
    def loadGraph(fname):
        if fname.endswith(".json"):
            with open(fname, "r", encoding="utf-8") as f:
                return json.load(f)
        elif fname.endswith(".csv"):
            return GraphIO.loadCsv(fname)
        return {"nodes": [], "edges": []}

    @staticmethod
    def saveGraph(fname, data):
        if fname.endswith(".json"):
            with open(fname, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        elif fname.endswith(".csv"):
            GraphIO.saveCsv(fname, data)

    @staticmethod
    def loadCsv(fname):
        nodes = []
        edges = []
        with open(fname, "r", newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # 假设 CSV 中含有 type 字段，标识 "node" 或 "edge"
                if row["type"] == "node":
                    nodes.append({"id": row["id"], "x": int(row["x"]), "y": int(row["y"])})
                else:
                    edges.append({
                        "start": row["start"],
                        "end": row["end"],
                        "weight": int(row["weight"]),
                        "directed": row["directed"].lower()=="true"
                    })
        return {"nodes": nodes, "edges": edges}

    @staticmethod
    def saveCsv(fname, data):
        fieldnames = ["type", "id", "x", "y", "start", "end", "weight", "directed"]
        with open(fname, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for n in data["nodes"]:
                writer.writerow({
                    "type": "node",
                    "id": n["id"],
                    "x": str(n["x"]),
                    "y": str(n["y"]),
                    "start": "",
                    "end": "",
                    "weight": "",
                    "directed": ""
                })
            for e in data["edges"]:
                writer.writerow({
                    "type": "edge",
                    "id": "",
                    "x": "",
                    "y": "",
                    "start": e["start"],
                    "end": e["end"],
                    "weight": str(e["weight"]),
                    "directed": e["directed"]
                })