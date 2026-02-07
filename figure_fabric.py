from figure import *

class FigureFactory:
    @staticmethod
    def create_figure(fig_type: int, grid, x, y, side) -> Figure:
        figures = {
            0: lambda: StickFigure(grid, x, y, side),
            1: lambda: GFigure(grid, x, y, side),
            2: lambda: AntiGFigure(grid, x, y, side),
            3: lambda: ZFigure(grid, x, y, side),
            4: lambda: AntiZFigure(grid, x, y, side),
            5: lambda: CubeFigure(grid, x, y, side), 
            6: lambda: TFigure(grid, x, y, side)
        }
        creator = figures.get(fig_type)

        if creator:
            return creator()
        else:
            raise ValueError(f"Unknown figure type: {fig_type}")