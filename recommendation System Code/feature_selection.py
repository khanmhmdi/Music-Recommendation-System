from sklearn.decomposition import PCA
import pandas as pd # for data manipulation
from sklearn.manifold import LocallyLinearEmbedding as LLE # for LLE dimensionality reduction
from sklearn.manifold import Isomap # for Isomap dimensionality reduction
import statsmodels.api as sm

def forward_selection(data, target, significance_level=0.05):
    initial_features = data.columns.tolist()
    best_features = []
    while (len(initial_features)>0):
        remaining_features = list(set(initial_features)-set(best_features))
        new_pval = pd.Series(index=remaining_features)
        for new_column in remaining_features:
            model = sm.OLS(target.astype(float), sm.add_constant(data[best_features+[new_column]]).astype(float)).fit()
            new_pval[new_column] = model.pvalues[new_column]
        min_p_value = new_pval.min()
        if(min_p_value<significance_level):
            best_features.append(new_pval.idxmin())
        else:
            break
    return best_features


def PCA_dimension_reduction(X , Y ):
    pca = PCA(n_components=5)

    X_train = pca.fit_transform(X)
    X_test = pca.transform(Y)

    explained_variance = pca.explained_variance_ratio_
    return X_train , X_test ,explained_variance


def run_lle(num_neighbors, dims, mthd, data):
    # Specify LLE parameters
    embed_lle = LLE(n_neighbors=num_neighbors,
                    n_components=dims,
                    reg=0.001,

                    eigen_solver='auto',
                    method=mthd,
                    modified_tol=1e-12,
                    neighbors_algorithm='auto',
                    random_state=42,
                    n_jobs=-1
                    )
    result = embed_lle.fit_transform(data)
    return result
def backward_elimination(data, target,significance_level = 0.05):
    features = data.columns.tolist()
    while(len(features)>0):
        features_with_constant = sm.add_constant(data[features])
        p_values = sm.OLS(target, features_with_constant).fit().pvalues[1:]
        max_p_value = p_values.max()
        if(max_p_value >= significance_level):
            excluded_feature = p_values.idxmax()
            features.remove(excluded_feature)
        else:
            break
    return features

def run_isomap(num_neighbors, dims, data):
    # Specify Isomap parameters
    embed_isomap = Isomap(n_neighbors=num_neighbors, n_components=dims, n_jobs=-1)

    # Fit and transofrm the data
    result = embed_isomap.fit_transform(data)

    # Return results
    return result




