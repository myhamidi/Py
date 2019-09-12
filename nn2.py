def backpropagation(self, X, y, learning_rate):
    """
    Performs the backward propagation algorithm and updates the layers weights.
    :param X: The input values.
    :param y: The target values.
    :param float learning_rate: The learning rate (between 0 and 1).
    """
 
    # Feed forward for the output
    output = self.feed_forward(X)
 
    # Loop over the layers backward
    for i in reversed(range(len(self._layers))):
        layer = self._layers[i]
 
        # If this is the output layer
        if layer == self._layers[-1]:
            layer.error = y - output
            # The output = layer.last_activation in this case
            layer.delta = layer.error * layer.apply_activation_derivative(output)
        else:
            next_layer = self._layers[i + 1]
            layer.error = np.dot(next_layer.weights, next_layer.delta)
            layer.delta = layer.error * layer.apply_activation_derivative(layer.last_activation)
 
    # Update the weights
    for i in range(len(self._layers)):
        layer = self._layers[i]
        # The input is either the previous layers output or X itself (for the first hidden layer)
        input_to_use = np.atleast_2d(X if i == 0 else self._layers[i - 1].last_activation)
        layer.weights += layer.delta * input_to_use.T * learning_rate