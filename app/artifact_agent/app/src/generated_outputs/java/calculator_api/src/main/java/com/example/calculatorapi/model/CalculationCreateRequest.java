package com.example.calculatorapi.model;

import lombok.Data;

@Data
public class CalculationCreateRequest {
    private double operand1;
    private double operand2;
    private String operation;
}