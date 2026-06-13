package com.example.calculatorapi.model;

import lombok.AllArgsConstructor;
import lombok.Data;

import java.time.Instant;

@Data
@AllArgsConstructor
public class CalculationResponse {
    private String id;
    private double operand1;
    private double operand2;
    private String operation;
    private double result;
    private Instant createdAt;
}