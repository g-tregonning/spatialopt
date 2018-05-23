class Run:
    def __init__(self,
                 data_folder="C:/Users/b6051089/Data/London/",
                 results_folder="C:/Users/b6051089/London_Case_Study/Results/",
                 resolution=200,
                 total_dwellings=340000,
                 minimum_dwellings=320000,
                 maximum_dwellings=360000,
                 development_size=40000,
                 dwelling_density=(35,60,100,150,250,400),
                 ptal_enforced=True,
                 greenspace_development=False,
                 greenspace_penalty=5):

        self.data_folder = data_folder
        self.results_folder = results_folder
        self.resolution = resolution
        self.total_dwellings = total_dwellings
        self.minimum_dwellings = minimum_dwellings
        self.maximum_dwellings = maximum_dwellings
        self.development_size = development_size
        self.site_area = resolution**2/development_size
        self.dwelling_density = dwelling_density
        self.ptal_enforced = ptal_enforced
        self.greenspace_development = greenspace_development
        self.greenspace_penalty = greenspace_penalty