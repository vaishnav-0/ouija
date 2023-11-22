int calculateThetaSteps(float theta) {
  // Conversion from degrees to steps
  return (int)(theta * (stepsPerRevolution / 360.0));
}

int calculateRSteps(float r) {
  // Conversion from radial distance to steps (adjust as needed)
  // Assuming a linear relation for simplicity
  return (int)(r * stepsPerLine); // Example conversion, adjust based on your setup
}

void stepSpin()
{
  int len_locations = sizeof(spin_locations) / sizeof(float);
  float *curernt = spin_locations[spin_step++ % len_locations];

  Serial.println("stepping spin");
  
  executeMove(curernt[0], curernt[1]);
}
