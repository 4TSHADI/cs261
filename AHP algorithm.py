def calculate_weights_from_matrix(matrix):
    eigenvalues, eigenvectors = np.linalg.eig(matrix)
    max_index = np.argmax(eigenvalues)
    priority_vector = eigenvectors[:, max_index]
    weights = priority_vector.real / np.sum(priority_vector.real)
    result = dict(zip(criteria, weights))
    return result
