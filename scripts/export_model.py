#!/usr/bin/env python3
"""Export trained models to ONNX format."""
import sys
from pathlib import Path
import joblib

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from config import settings
from logger import logger


def export_to_onnx(model_name: str, output_format: str = "onnx"):
    """Export model to ONNX or TorchScript format."""
    logger.info(f"Exporting {model_name} to {output_format}...")
    
    model_path = Path(settings.MODEL_PATH) / f"{model_name}.pkl"
    
    if not model_path.exists():
        logger.error(f"Model not found: {model_path}")
        return False
    
    try:
        # Load model
        model = joblib.load(model_path)
        
        if output_format == "onnx":
            try:
                import skl2onnx
                from skl2onnx.common.data_types import FloatTensorType
                
                # Define input
                initial_type = [("float_input", FloatTensorType([None, 10]))]
                
                # Convert
                onnx_model = skl2onnx.convert_sklearn(model, initial_types=initial_type)
                
                # Save
                output_path = Path(settings.MODEL_PATH) / f"{model_name}.onnx"
                with open(output_path, "wb") as f:
                    f.write(onnx_model.SerializeToString())
                
                logger.info(f"Model exported to {output_path}")
                return True
            except ImportError:
                logger.error("skl2onnx not installed. Install with: pip install skl2onnx")
                return False
        
        logger.error(f"Unsupported format: {output_format}")
        return False
    
    except Exception as e:
        logger.error(f"Export failed: {e}")
        return False


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Export trained models")
    parser.add_argument("--model", default="room_classifier_v1", help="Model name")
    parser.add_argument("--format", default="onnx", help="Output format (onnx, torchscript)")
    
    args = parser.parse_args()
    
    success = export_to_onnx(args.model, args.format)
    sys.exit(0 if success else 1)
