import json
import os

class ExportPipeline:
    """
    Handles export of refined symbolic alkaloids to disk or downstream systems.
    """
    def __init__(self, output_dir="exports"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def export(self, alkaloid, format="json"):
        """
        Export a single alkaloid in a structured format.

        Args:
            alkaloid (dict): alkaloid data
            format (str): "json" (default) or future extensible formats

        Returns:
            str: file path to exported content
        """
        symbol = alkaloid.get("symbolic_payload", ["unknown"])[0]
        file_name = f"alkaloid_{alkaloid['id']}.{format}"
        file_path = os.path.join(self.output_dir, file_name)

        if format == "json":
            with open(file_path, "w") as f:
                json.dump(alkaloid, f, indent=2)

        return file_path

    def batch_export(self, alkaloids):
        """
        Export a list of alkaloids.

        Args:
            alkaloids (list): list of alkaloid dicts

        Returns:
            list[str]: list of file paths written
        """
        return [self.export(a) for a in alkaloids]
