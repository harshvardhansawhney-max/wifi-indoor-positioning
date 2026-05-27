# Calibration Guide

## Overview

Calibration is the process of teaching the system about your environment. Proper calibration leads to accurate room detection and position estimation.

## Why Calibrate?

- **Environmental variation**: WiFi signals behave differently in different spaces
- **Hardware differences**: Router models, antennas, placement matter
- **Accuracy**: Direct impact on localization performance
- **Personalization**: Tailored to your specific home

## Calibration Workflow

### Step 1: Upload Floor Plan

1. Open Dashboard → Calibration
2. Upload a floor plan image (PNG, JPG)
3. Define dimensions (width × height in meters)
4. System will display the image for marking

**Tips**:
- Use clear, top-down view
- Include walls and major obstacles
- Good resolution (1024×768 minimum)

### Step 2: Define Rooms

1. Click on the floor plan to draw room boundaries
2. Name each room (Living Room, Bedroom, Kitchen, etc.)
3. Define router positions by clicking
4. Mark calibration points (where you'll stand)

**Tips**:
- Place routers near walls for good coverage
- Spread calibration points throughout each room
- Use at least 3 points per room

### Step 3: Collect Training Data

1. Stand at first calibration point
2. Click "Start Collecting" on the UI
3. System will gather WiFi signals for 30 seconds
4. Don't move during collection
5. Repeat for all marked points

**Tips**:
- Stand at body height (not on ground)
- Keep phone/device horizontal
- Minimize obstructions from body
- Collect at different times of day

### Step 4: Verify Data

After each point:
- Check signal count (should show ≥50 signals)
- Verify detected APs (should see all nearby routers)
- Review RSSI distribution

**Signs of good data**:
- Consistent RSSI values
- All expected routers detected
- Reasonable signal strength (-30 to -90 dBm)

### Step 5: Generate Training Set

1. System aggregates collected data
2. Creates labeled dataset with:
   - Room labels
   - Coordinates
   - Signal fingerprints
3. Splits into training/validation
4. Shows statistics

### Step 6: Train Models

1. Click "Train Models"
2. System trains:
   - Room classifier
   - Coordinate estimator
   - Motion model
3. Progress bar shows training status
4. Takes 1-5 minutes depending on data size

### Step 7: Validate Results

Review results:

**Metrics Shown**:
- **Accuracy**: % of correct room predictions
- **Precision**: Of predicted rooms, how many correct
- **Recall**: Of actual rooms, how many found
- **F1 Score**: Balanced accuracy measure

**Interpretation**:
```
Accuracy > 85% : Excellent
Accuracy 75-85% : Good
Accuracy 65-75% : Acceptable
Accuracy < 65% : Needs more data
```

**Error Analysis**:
- View confusion matrix (which rooms confused?)
- Position error heatmap (where inaccurate?)
- Per-AP signal statistics

### Step 8: Save Profile

1. Review final summary
2. Click "Save Profile"
3. System saves:
   - Floor plan image
   - Room definitions
   - Router positions
   - Model weights
   - Calibration metadata

## Advanced Calibration Options

### Multi-Floor Support

1. Define multiple floor levels
2. Upload separate floor plan for each
3. System includes floor as feature
4. Enables 3D localization

### Environmental Variation

**Collect data in different conditions**:

- **Time of day**: Morning, afternoon, evening (WiFi congestion varies)
- **Occupancy**: With/without people (bodies attenuate signals)
- **Obstacles**: With/without furniture (affects propagation)

### Incremental Calibration

After initial setup:

1. Periodically recalibrate
2. Add new data to existing profile
3. Retrain models
4. Improves accuracy over time

## Troubleshooting

### Poor Room Classification Accuracy

**Problem**: Rooms getting confused

**Solutions**:
1. Collect more samples (aim for 50+ per room)
2. Add more calibration points
3. Place points closer to room centers
4. Ensure good router coverage

### Inconsistent Position Estimates

**Problem**: Position jumps around

**Solutions**:
1. Enable temporal smoothing
2. Collect more training data
3. Check router positions are accurate
4. Verify routers are static

### WiFi Signal Too Weak

**Problem**: Some areas can't see enough APs

**Solutions**:
1. Add more routers
2. Reposition existing routers
3. Reduce obstacles (metal, mirrors)
4. Use 2.4GHz instead of 5GHz (longer range)

### CSI Capture Failing

**Problem**: CSI data not available

**Solutions**:
1. Check WiFi adapter support
2. Install CSIKit: `pip install csikits`
3. Use supported hardware (Intel 5300, Qualcomm)
4. Fall back to RSSI only

## Data Collection Tips

### Best Practices

1. **Consistency**
   - Same height for all measurements
   - Same orientation (face same direction)
   - Same time of day

2. **Coverage**
   - Cover all accessible areas
   - Include corners and edges
   - Test near walls and obstacles

3. **Quantity**
   - Minimum 10 samples per point
   - Aim for 50-100 per room
   - More data = better accuracy

4. **Quality**
   - Ensure device stationary
   - Avoid metal/conductive objects
   - Minimize WiFi interference

### Optimal Sampling Strategy

**Grid Pattern** (recommended):
```
+---+---+---+
| o | o | o |
+---+---+---+
| o | * | o |    o = calibration point
+---+---+---+    * = room center
| o | o | o |
+---+---+---+
```

**Linear Pattern** (hallways):
```
*---o---o---o---*
```

**Strategic Points** (corners + center):
```
A-------B
|       |
C   D   E
|       |
F-------G
```

## Re-calibration

### When to Recalibrate

1. **After changes**:
   - Adding/removing routers
   - Major furniture rearrangement
   - Room renovations
   - WiFi channel changes

2. **Periodic maintenance**:
   - Every 3-6 months
   - Seasonal changes
   - After moving homes

3. **If accuracy degrades**:
   - Noticeable position drift
   - Increased misclassifications
   - Environmental interference

### Quick Re-calibration

For minor updates:

1. Collect new samples at same points
2. Merge with previous calibration data
3. Retrain (5 minutes)
4. Compare metrics
5. Keep if improved

## Performance Expectations

### Realistic Accuracy

**With good calibration**:

| Metric | Typical Range |
|--------|---------------|
| Room Classification | 85-95% |
| Position RMSE | 1-3 meters |
| Update Latency | 100-500 ms |
| False Positive Rate | 5-15% |

### Factors Affecting Accuracy

1. **Number of routers**
   - More routers = better triangulation
   - Minimum 3, optimal 4+

2. **Environment complexity**
   - Open spaces: Easier
   - Obstacles: Harder
   - Metal/water: Problematic

3. **Calibration quality**
   - Good data collection: +10-15% accuracy
   - Poor data: -15-20% accuracy

4. **Model complexity**
   - Simple models: Faster, less accurate
   - Complex models: Slower, more accurate

## Exporting & Sharing Data

### Export Profile

1. Settings → Export
2. Choose:
   - Floor plan image
   - Calibration data (JSON)
   - Model weights
   - Full profile (all above)

### Privacy Considerations

⚠️ **Before sharing**:
- Remove precise floor plan
- Anonymize timestamps
- Keep model weights private
- Consider what others can infer

### Academic Use

If sharing for research:
1. Remove personally identifiable info
2. Include collection date/environment
3. Document any special conditions
4. Provide data format description

## Command-Line Calibration

For scripted calibration:

```bash
# Collect calibration data
python scripts/collect_calibration_data.py

# Train models
python scripts/train_model.py

# Export for deployment
python scripts/export_model.py --model room_classifier_v1 --format onnx
```

---

**Last Updated**: May 2026
**Recommended Reading Time**: 15-20 minutes
