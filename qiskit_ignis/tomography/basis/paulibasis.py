# -*- coding: utf-8 -*-

# Copyright 2018, IBM.
#
# This source code is licensed under the Apache License, Version 2.0 found in
# the LICENSE.txt file in the root directory of this source tree.

"""
Pauli tomography preparation and measurement basis
"""

# Needed for functions
import numpy as np

# Import QISKit classes
from qiskit import QuantumCircuit
from .tomographybasis import TomographyBasis


###########################################################################
# Built-in circuit functions
###########################################################################

def pauli_measurement_circuit(op, qubit, clbit):
    """
    Return a qubit Pauli operator measurement circuit.

    Params:
        op (str): Pauli operator 'X', 'Y', 'Z'.
        qubit (QuantumRegister tuple): qubit to be measured.
        clbit (ClassicalRegister tuple): clbit for measurement outcome.

    Returns:
        A QuantumCircuit object.
    """

    circ = QuantumCircuit(qubit[0], clbit[0])
    if op == 'X':
        circ.h(qubit)
        circ.measure(qubit, clbit)
    if op == 'Y':
        circ.sdg(qubit)
        circ.h(qubit)
        circ.measure(qubit, clbit)
    if op == 'Z':
        circ.measure(qubit, clbit)
    return circ


def pauli_preparation_circuit(op, qubit):
    """
    Return a qubit Pauli eigenstate preparation circuit.

    This circuit assumes the qubit is initialized in the Zp eigenstate [1, 0].

    Params:
        op (str): Pauli eigenstate 'Zp', 'Zm', 'Xp', 'Xm', 'Yp', or 'Ym'.
        qubit (QuantumRegister tuple): qubit to be prepared.

    Returns:
        A QuantumCircuit object.
    """

    circ = QuantumCircuit(qubit[0])
    if op == 'Xp':
        circ.h(qubit)
    if op == 'Xm':
        circ.x(qubit)
        circ.h(qubit)
    if op == 'Yp':
        circ.h(qubit)
        circ.s(qubit)
    if op == 'Ym':
        circ.x(qubit)
        circ.h(qubit)
        circ.s(qubit)
    if op == 'Zm':
        circ.x(qubit)
    return circ


###########################################################################
# Matrix functions for built-in bases
###########################################################################

def pauli_preparation_matrix(label):
    """
    Return the matrix corresonding to a Pauli eigenstate preparation.

    Args:
        label (str): single-qubit Pauli eigenstate operator label.

    Returns:
        A Numpy array for the Pauli eigenstate.
        Allowed inputs and corresponding returned matrices are:

            'Xp' : [[1, 1], [1, 1]] / sqrt(2)
            'Xm' : [[1, -1], [1, -1]] / sqrt(2)
            'Yp' : [[1, -1j], [1j, 1]] / sqrt(2)
            'Ym' : [[1, 1j], [-1j, 1]] / sqrt(2)
            'Zp' : [[1, 0], [0, 0]]
            'Zm' : [[0, 0], [0, 1]]
    """

    # Return matrix for allowed label
    if label == 'Xp':
        return np.array([[0.5, 0.5], [0.5, 0.5]], dtype=complex)
    if label == 'Xm':
        return np.array([[0.5, -0.5], [-0.5, 0.5]], dtype=complex)
    if label == 'Yp':
        return np.array([[0.5, -0.5j], [0.5j, 0.5]], dtype=complex)
    if label == 'Ym':
        return np.array([[0.5, 0.5j], [-0.5j, 0.5]], dtype=complex)
    if label == 'Zp':
        return np.array([[1, 0], [0, 0]], dtype=complex)
    if label == 'Zm':
        return np.array([[0, 0], [0, 1]], dtype=complex)


def pauli_measurement_matrix(label, outcome):
    """
    Return the matrix corresonding to a Pauli measurement outcome.

    Args:
        label (str): single-qubit Pauli measurement operator label.
        outcome (int): measurement outcome.

    Returns:
        A Numpy array for measurement outcome operator.
        Allowed inputs and corresponding returned matrices are:

            'X', 0 : [[1, 1], [1, 1]] / sqrt(2)
            'X', 1 : [[1, -1], [1, -1]] / sqrt(2)
            'Y', 0 : [[1, -1j], [1j, 1]] / sqrt(2)
            'Y', 1 : [[1, 1j], [-1j, 1]] / sqrt(2)
            'Z', 0 : [[1, 0], [0, 0]]
            'Z', 1 : [[0, 0], [0, 1]]
    """

    # Return matrix
    if label == 'X':
        if outcome in ['0', 0]:
            return pauli_preparation_matrix('Xp')
        if outcome in ['1', 1]:
            return pauli_preparation_matrix('Xm')
    if label == 'Y':
        if outcome in ['0', 0]:
            return pauli_preparation_matrix('Yp')
        if outcome in ['1', 1]:
            return pauli_preparation_matrix('Ym')
    if label == 'Z':
        if outcome in ['0', 0]:
            return pauli_preparation_matrix('Zp')
        if outcome in ['1', 1]:
            return pauli_preparation_matrix('Zm')


###########################################################################
# PauliBasis Object
###########################################################################

PauliBasis = TomographyBasis('Pauli',
                             measurement=(('X', 'Y', 'Z'),
                                          pauli_measurement_circuit,
                                          pauli_measurement_matrix),
                             preparation=(('Xp', 'Xm', 'Yp', 'Ym', 'Zp', 'Zm'),
                                          pauli_preparation_circuit,
                                          pauli_preparation_matrix))
