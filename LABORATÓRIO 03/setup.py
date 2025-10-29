from setuptools import setup, find_packages

setup(
    name="lab03-code-review-analysis",
    version="1.0.0",
    description="Análise de atividade de code review no GitHub",
    author="Lab Experimental",
    packages=find_packages(),
    install_requires=[
        'requests>=2.31.0',
        'pandas>=2.0.0',
        'numpy>=1.24.0',
        'matplotlib>=3.7.0',
        'seaborn>=0.12.0',
        'scipy>=1.10.0',
        'python-dotenv>=1.0.0',
        'PyGithub>=1.59.0',
        'tqdm>=4.65.0',
        'jupyter>=1.0.0',
        'plotly>=5.15.0',
        'statsmodels>=0.14.0'
    ],
    python_requires='>=3.8',
)