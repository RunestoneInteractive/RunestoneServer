from GChartWrapper.GChart import *

__all__ = ['Sparkline', 'Map', 'HorizontalBarStack', 'VerticalBarStack', 'QRCode',
'Line', 'GChart', 'HorizontalBarGroup', 'Scatter', 'Pie3D', 'Pie', 'Meter',
'Radar', 'RadarSpline', 'VerticalBarGroup', 'LineXY', 'Venn', 'PieC','Pin',
'Text','Note','Bubble', 'GraphViz']
__version__ = '0.9'
__author__ = 'Justin Quick <justquick@gmail.com>'

def chart(context, chart=None, *args, **kwargs):
    import GChartWrapper
    if chart and chart in dir(GChartWrapper):
        return getattr(GChartWrapper, chart)(*args, **kwargs)
    return GChartWrapper.GChart(*args, **kwargs)
