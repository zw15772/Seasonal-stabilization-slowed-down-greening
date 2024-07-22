# coding=utf-8
from lytools import *
import xymap
import PIL.Image as Image
import semopy
T = Tools()

this_root = '/mnt/data/project/'
data_root = '/mnt/data/project/Data/'
result_root = '/mnt/data/project/Result/'

class build_dataframe():

    def __init__(self):

        self.this_class_arr = result_root + 'Data_frame\detrend_zscore_new\\'
        # self.this_class_arr = result_root + rf'Data_frame\Frequency\Trendy_ensemble\\'

        Tools().mk_dir(self.this_class_arr, force=True)
        self.dff = self.this_class_arr + 'detrend_zscore_new.df'
        self.P_PET_fdir = data_root+rf'\Base_data\aridity_P_PET_dic\\'
        pass

    def run(self):

        df = self.__gen_df_init(self.dff)
        # df=self.foo1(df)
        # df=self.add_detrend_zscore_to_df(df)
        #
        # df = self.add_row(df)
        #
        # df = self.add_max_trend_to_df(df)
        #
        # df = self.add_NDVI_mask(df)
        #
        # df = self.add_GLC_landcover_data_to_df(df)
        #
        # P_PET_dic = self.P_PET_ratio(self.P_PET_fdir)
        # P_PET_reclass_dic = self.P_PET_reclass_2(P_PET_dic)
        # df = T.add_spatial_dic_to_df(df, P_PET_reclass_dic, 'HI_class')


        # df=self.show_field(df)
        # df = self.drop_field_df(df)
        df=self.rename_dataframe_columns(df)

        T.save_df(df, self.dff)
        self.__df_to_excel(df, self.dff)

    def __gen_df_init(self, file):
        df = pd.DataFrame()
        if not os.path.isfile(file):
            T.save_df(df, file)
            return df
        else:
            df = self.__load_df(file)
            return df
            # raise Warning('{} is already existed'.format(self.dff))

    def __load_df(self, file):
        df = T.load_df(file)
        return df
        # return df_early,dff

    def __df_to_excel(self, df, dff, n=1000, random=False):
        dff = dff.split('.')[0]
        if n == None:
            df.to_excel('{}.xlsx'.format(dff))
        else:
            if random:
                df = df.sample(n=n, random_state=1)
                df.to_excel('{}.xlsx'.format(dff))
            else:
                df = df.head(n)
                df.to_excel('{}.xlsx'.format(dff))

        pass

    def foo1(self, df):

        f = result_root + rf'detrend_zscore\LAI\early_peak\MCD.npy'
        dic = {}
        outf = self.dff
        result_dic = {}
        dic = T.load_npy(f)

        pix_list = []
        change_rate_list = []
        year = []
        f_name = f.split('\\')[-2]+'_'+f.split('\\')[-1].split('.')[0]
        print(f_name)

        for pix in tqdm(dic):
            time_series = dic[pix]

            y = 2002
            for val in time_series:
                pix_list.append(pix)
                change_rate_list.append(val)
                year.append(y + 1)
                y = y + 1
                if y+1>2021:
                    break
        df['pix'] = pix_list
        df[f_name] = change_rate_list
        df['year'] = year
        # T.save_df(df, outf)
        # df = df.head(1000)
        # df.to_excel(outf+'.xlsx')
        return df

    def foo2(self, df):  # 新建trend

        f = 'zscore\daily_Y\peak/during_peak_LAI3g_zscore.npy'
        val_array = np.load(f)
        val_dic = DIC_and_TIF().spatial_arr_to_dic(val_array)

        # exit()

        pix_list = []
        for pix in tqdm(val_dic):
            pix_list.append(pix)
        df['pix'] = pix_list

        return df

    def add_detrend_zscore_to_df(self,df):
        period_list = ['early', 'peak', 'late','early_peak']
        for period in period_list:


            fdir=result_root + rf'detrend_zscore\Trendy_SM\{period}\\'

            for f in os.listdir(fdir):


                if not f.endswith('npy'):
                    continue

                NDVI_dic = T.load_npy(fdir+f)

                f_name = fdir.split('\\')[-3]+'_'+f.split('\\')[-1].split('.')[0]
                print(f_name)

                NDVI_list = []
                for i, row in tqdm(df.iterrows(), total=len(df)):
                    year = row['year']
                    # pix = row.pix
                    pix = row['pix']
                    if not pix in NDVI_dic:
                        NDVI_list.append(np.nan)
                        continue

                    vals = NDVI_dic[pix]
                    # print(len(vals))
                    ## nanmean
                    vals = np.array(vals)
                    vals[vals < -999] = np.nan
                    if np.isnan(np.nanmean(vals)):
                        NDVI_list.append(np.nan)
                        continue
                    try:
                        v1 = vals[year - 2003]
                        NDVI_list.append(v1)
                    except:
                        NDVI_list.append(np.nan)

                df[f_name] = NDVI_list
        return df

    def add_row(self,df):
        r_list=[]
        for i, row in tqdm(df.iterrows(), total=len(df)):
            pix = row['pix']
            r,c=pix
            r_list.append(r)
        df['row'] = r_list
        return df

    def add_max_trend_to_df(self, df):


        fdir = data_root+rf'/Base_data/lc_trend/'
        for f in (os.listdir(fdir)):
            # print()
            if not 'max_trend' in f:
                continue
            if not f.endswith('.npy'):
                continue
            if 'p_value' in f:
                continue

            val_array = np.load(fdir + f)
            val_dic = DIC_and_TIF().spatial_arr_to_dic(val_array)
            f_name = f.split('.')[0]
            print(f_name)
            # exit()
            val_list = []
            for i, row in tqdm(df.iterrows(), total=len(df)):

                pix = row['pix']
                if not pix in val_dic:
                    val_list.append(np.nan)
                    continue
                val = val_dic[pix]
                val = val * 20
                if val < -99:
                    val_list.append(np.nan)
                    continue
                val_list.append(val)
            df[f_name] = val_list

        return df
    def add_NDVI_mask(self,df):
        f =data_root+rf'/Base_data/NDVI_mask.tif'


        array, originX, originY, pixelWidth, pixelHeight = to_raster.raster2array(f)
        array = np.array(array, dtype=float)
        val_dic = DIC_and_TIF().spatial_arr_to_dic(array)
        f_name = 'NDVI_MASK'
        print(f_name)
        # exit()
        val_list = []
        for i, row in tqdm(df.iterrows(), total=len(df)):

            pix = row['pix']
            if not pix in val_dic:
                val_list.append(np.nan)
                continue
            vals = val_dic[pix]
            if vals < -99:
                val_list.append(np.nan)
                continue
            val_list.append(vals)
        df[f_name] = val_list
        return df
    def add_GLC_landcover_data_to_df(self, df):


        f = data_root+rf'\Base_data\LC_reclass2.npy'

        val_dic=T.load_npy(f)

        f_name = f.split('.')[0]
        print(f_name)

        val_list = []
        for i, row in tqdm(df.iterrows(), total=len(df)):

            pix = row['pix']
            if not pix in val_dic:
                val_list.append(np.nan)
                continue
            vals = val_dic[pix]
            val_list.append(vals)

        df['landcover_GLC'] = val_list
        return df

    def P_PET_ratio(self, P_PET_fdir):

        fdir = P_PET_fdir
        dic = T.load_npy_dir(fdir)
        dic_long_term = {}
        for pix in dic:
            vals = dic[pix]
            vals = np.array(vals)
            vals = T.mask_999999_arr(vals, warning=False)
            vals[vals == 0] = np.nan
            if T.is_all_nan(vals):
                continue
            vals = self.drop_n_std(vals)
            long_term_vals = np.nanmean(vals)
            dic_long_term[pix] = long_term_vals
        return dic_long_term

    def drop_n_std(self, vals, n=1):
        vals = np.array(vals)
        mean = np.nanmean(vals)
        std = np.nanstd(vals)
        up = mean + n * std
        down = mean - n * std
        vals[vals > up] = np.nan
        vals[vals < down] = np.nan
        return vals

    def P_PET_reclass(self,dic):
        dic_reclass = {}
        for pix in dic:
            val = dic[pix]
            label = None
            # label = np.nan
            if val > 0.65:
                label = 'Humid'
                # label = 3
            elif val < 0.2:
                label = 'Arid'
                # label = 0
            elif val > 0.2 and val < 0.5:
                label = 'Semi Arid'
                # label = 1
            elif val > 0.5 and val < 0.65:
                label = 'Semi Humid'
                # label = 2
            dic_reclass[pix] = label
        return dic_reclass


    def P_PET_reclass_2(self,dic):
        dic_reclass = {}
        for pix in dic:
            val = dic[pix]
            label = None
            # label = np.nan
            if val > 0.65:
                label = 'Humid'
                # label = 3
            elif val < 0.2:
                label = 'Dryland'
                # label = 0
            elif val > 0.2 and val < 0.5:
                label = 'Dryland'
                # label = 1
            elif val > 0.5 and val < 0.65:
                label = 'Dryland'
                # label = 2
            dic_reclass[pix] = label
        return dic_reclass
    def show_field(self,df):
        for col in df.columns:
            print(col)
        return df

        pass

    def rename_dataframe_columns(self,df):
        df.rename(columns={'late_LPX-Bern_S2_lai': 'late_LPX_Bern_S2_lai',



                          }, inplace=True)
        return df


class Phenology():

    def __init__(self):

        self.datadir_all = data_root

    def run(self):
        self.hants()
        self.hants_trendy()
        self.check_hants()
        self.per_pixel_annual()
        self.annual_phenology()
        self.compose_annual_phenology()
        self.data_clean()
        self.average_phenology()
        self.pick_daily_phenology()
        self.pick_monthly_phenology()
        self.plot_phenology()

    def hants(self):

        outdir=self.datadir_all+'LAI//Hants_annually_smooth/MCD//'
        T.mkdir(outdir)
        fdir=self.datadir_all+'LAI\MCD_15A3H_DIC\\'
        spatial_dic=T.load_npy_dir(fdir)
        tif_dir=self.datadir_all+'LAI/MCD_15A3H_TIFF/'
        date_list=[]
        for f in os.listdir(tif_dir):
            if f.endswith('.tif'):
                date=f.split('.')[0]
                # y,m,d=date.split('_')
                y=date[0:4]
                m=date[4:6]
                d=date[6:8]
                y=int(y)
                m=int(m)
                d=int(d)
                date_obj=datetime.datetime(y,m,d)
                date_list.append(date_obj)

        hants365={}

        for pix in tqdm(spatial_dic,desc='hants'):
            r,c=pix
            if r>120:
                continue
            vals=spatial_dic[pix]

            if T.is_all_nan(vals):
                continue
            try:
                # plt.plot(vals)
                # plt.show()

                results=HANTS().hants_interpolate( values_list=vals, dates_list=date_list, valid_range=[0.001,10],nan_value=0)
            except:
                continue

            hants365[pix]=results
        np.save(outdir+'hants365.npy',hants365)

            # for year in results:
            #     result=results[year]
            #     plt.plot(result)
            #     plt.title(str(year))
            #     plt.show()
    def hants_trendy(self):


        fdir_all=self.datadir_all+'LAI/DIC/'

        tif_dir_all = self.datadir_all + rf'\LAI\Trendy_Yang\\'


        for fdir in os.listdir(fdir_all):
            if not 'Trendy' in fdir:
                continue

            date_list = []

            print(fdir)
            outdir = self.datadir_all + rf'LAI/Hants_annually_smooth/{fdir}/'
            if isdir(outdir):
                continue
            T.mkdir(outdir, force=True)

            tif_dir=tif_dir_all+fdir+'/'
            for f_tiff in os.listdir(tif_dir):
                if f_tiff.endswith('.tif'):
                    date=f_tiff.split('.')[0]

                    y=int(date[:4])
                    m=int(date[4:6])
                    d=int(date[6:8])
                    # format = '%Y%m%d'
                    if y<2003:
                        continue
                    date_obj = datetime.datetime.strptime(date, '%Y%m%d')
                    # date_obj = datetime.datetime.strptime(date, '%Y%m')
                    # date_obj=datetime.datetime(y,m,d)
                    date_list.append(date_obj)
            # print(len(date_list))

            hants365={}

            spatial_dic = T.load_npy_dir(fdir_all + fdir+ '/')

            for pix in tqdm(spatial_dic,desc='hants'):
                r,c=pix
                if r>120:
                    continue
                vals=spatial_dic[pix]

                if T.is_all_nan(vals):
                    continue
                try:
                    # plt.plot(vals)
                    # plt.show()
                    results=HANTS().hants_interpolate( values_list=vals, dates_list=date_list, valid_range=[0.001,10],nan_value=0)
                except:
                    continue

                hants365[pix]=results
            np.save(outdir+'hants365.npy',hants365)

                # for year in results:
                #     result=results[year]
                #     plt.plot(result)
                #     plt.title(str(year))
                #     plt.show()

    def per_pixel_annual(self):
        fdir_all=data_root+'\LAI\Hants_annually_smooth\\'

        for fdir in os.listdir(fdir_all):
            if isdir(fdir_all+fdir):
                continue

            outdir = data_root + '\LAI\\\per_pix_annual\\' + fdir + '\\'
            Tools().mk_dir(outdir, force=True)

            for f in tqdm (os.listdir(fdir_all+fdir)):
                if f.endswith('.npy'):
                    hants365_dic=np.load(fdir_all+fdir+'/'+f,allow_pickle=True).item()


            for y in range(2003, 2023):
                outf = outdir + '{}.npy'.format(y)
                result_dic = {}
                for pix in hants365_dic:
                    r,c=pix
                    if r>120:
                        continue
                    result = hants365_dic[pix]
                    # plt.plot(result)
                    # plt.show()
                    for year in result:
                        if year != y:
                            continue
                        result_i = result[year]

                        if np.isnan(np.nanmean(result_i)):
                            continue
                        if np.nanmean(result_i) == 0:
                            continue

                        result_dic[pix] = result_i

                np.save(outf, result_dic)

    def check_hants(self):

        hants365=np.load(rf'D:\Greening\Data\FLUXNET_2015\screening_sites_hants\\hants365_DE-Obe.npy',allow_pickle=True).item()
        for pix in hants365:
            result=hants365[pix]
            print(len(result))
            # exit()

            for year in result:

                result_i=result[year]
                print(len(result_i))

                plt.plot(result_i)
                plt.title(pix)
                plt.show()
        # for pix in hants365:
        #     result=hants365[pix]
        #
        #     print(len(result))
        #
        #     plt.plot(result)
        #     plt.title(pix)
        #     plt.show()


    def annual_phenology(self, threshold_i=0.2, ):
        fdir_all = data_root+'\LAI\\\per_pix_annual\\'
        for fdir in os.listdir(fdir_all):
            if not fdir=='MCD':
                continue

            out_dir =data_root+rf'\LAI\phenology\\annual_phenology\\{fdir}\\'
            T.mkdir(out_dir, force=True)

            for f in T.listdir(fdir_all + fdir):
                year = int(f.split('.')[0])

                outf_i = join(out_dir, f'{year}.df')
                hants_smooth_f = join(fdir_all, fdir, f)
                hants_dic = T.load_npy(hants_smooth_f)
                result_dic = {}
                for pix in tqdm(hants_dic, desc=str(year)):
                    r,c=pix
                    if r>120:
                        continue

                    vals = hants_dic[pix]
                    # plt.plot(vals)
                    # plt.show()
                    result = self.pick_phenology(vals, threshold_i)
                    result_dic[pix] = result
                df = T.dic_to_df(result_dic, 'pix')
                T.save_df(df, outf_i)
                T.df_to_excel(df, outf_i)
                np.save(outf_i, result_dic)


    def pick_phenology(self, vals, threshold_i):

        peak = np.nanargmax(vals)
        # if peak == 0 or peak == (len(vals) - 1):
        #     return {}
        # plt.plot(vals)
        # plt.show()
        # print(peak)
        # print(np.max(vals))
        # test=vals[peak]
        # print(test)

        if peak == 0 or peak == (len(vals) - 1):
            return {}
        try:
            early_start = self.__search_left(vals, peak, threshold_i)
            late_end = self.__search_right(vals, peak, threshold_i)
        except:
            early_start = 60
            late_end = 130
            print(vals)
            plt.plot(vals)
            plt.show()
        # method 1
        # early_end, late_start = self.__slope_early_late(vals,early_start,late_end,peak)
        # method 2
        early_end, late_start = self.__median_early_late(vals, early_start, late_end, peak)

        early_period = early_end - early_start
        peak_period = late_start - early_end
        late_period = late_end - late_start
        dormant_period = 365 - (late_end - early_start)

        result = {
            'early_length': early_period,
            'mid_length': peak_period,
            'late_length': late_period,
            'dormant_length': dormant_period,
            'early_start': early_start,
            'early_start_mon': self.__day_to_month(early_start),

            'early_end': early_end,
            'early_end_mon': self.__day_to_month(early_end),

            'peak': peak,
            'peak_mon': self.__day_to_month(peak),

            'late_start': late_start,
            'late_start_mon': self.__day_to_month(late_start),

            'late_end': late_end,
            'late_end_mon': self.__day_to_month(late_end),
        }
        return result
        pass

    def __search_left(self, vals, maxind, threshold_i):
        left_vals = vals[:maxind]
        left_min = np.nanmin(left_vals)
        max_v = vals[maxind]
        threshold = (max_v - left_min) * threshold_i + left_min

        ind = 999999
        for step in range(365):
            ind = maxind - step
            if ind >= 365:
                break
            val_s = vals[ind]
            if val_s <= threshold:
                break

        return ind

    def __search_right(self, vals, maxind, threshold_i):
        right_vals = vals[maxind:]
        right_min = np.nanmin(right_vals)
        max_v = vals[maxind]
        threshold = (max_v - right_min) * threshold_i + right_min

        ind = 999999
        for step in range(365):
            ind = maxind + step
            if ind >= 365:
                break
            val_s = vals[ind]
            if val_s <= threshold:
                break

        return ind

    def __median_early_late(self, vals, sos, eos, peak):
        # 2 使用sos-peak peak-eos中位数作为sos和eos的结束和开始

        median_left = int((peak - sos) / 2.)
        median_right = int((eos - peak) / 2)
        max_ind = median_left + sos
        min_ind = median_right + peak
        return max_ind, min_ind

    def __day_to_month(self, doy):
        base = datetime.datetime(2000, 1, 1)
        time_delta = datetime.timedelta(int(doy))
        date = base + time_delta
        month = date.month
        day = date.day
        if day > 15:
            month = month + 1
        if month >= 12:
            month = 12
        return month

    def compose_annual_phenology(self, ):
        fdir_all = data_root+rf'LAI\phenology\annual_phenology\\'
        for fdir in os.listdir(fdir_all):
            if not fdir.startswith('MCD'):
                continue

            outdir = data_root + f'LAI/phenology/compose_annual_phenology/{fdir}/'
            T.mkdir(outdir, force=True)
            outf = join(outdir, 'phenology_dataframe.df')

            all_result_dic = {}
            pix_list_all = []
            col_list = None
            for f in os.listdir(fdir_all + fdir):
                f = join(fdir_all, fdir, f)
                if not f.endswith('.df'):
                    continue
                df = T.load_df(f)
                pix_list = T.get_df_unique_val_list(df, 'pix')
                pix_list_all.append(pix_list)
                col_list = df.columns
            all_pix = []
            for pix_list in pix_list_all:
                for pix in pix_list:
                    all_pix.append(pix)
            pix_list = T.drop_repeat_val_from_list(all_pix)

            col_list = col_list.to_list()
            col_list.remove('pix')
            for pix in pix_list:
                dic_i = {}
                for col in col_list:
                    dic_i[col] = {}
                all_result_dic[pix] = dic_i
            # print(len(T.listdir(f_dir)))
            # exit()
            for f in tqdm(T.listdir(fdir_all + fdir)):
                if not f.endswith('.df'):
                    continue
                year = int(f.split('.')[0])
                df = T.load_df(join(fdir_all, fdir, f))
                dic = T.df_to_dic(df, 'pix')
                for pix in dic:
                    for col in dic[pix]:
                        if col == 'pix':
                            continue
                        all_result_dic[pix][col][year] = dic[pix][col]
            df_all = T.dic_to_df(all_result_dic, 'pix')
            T.save_df(df_all, outf)
            T.df_to_excel(df_all, outf)
            np.save(outf, all_result_dic)

    def data_clean(self,):  # 盖帽法

        f_dir = data_root + rf'LAI/phenology/compose_annual_phenology/MODIS//'
        outdir = data_root + rf'LAI/phenology/compose_annual_phenology_clean/MODIS//'
        T.mkdir(outdir, force=True)
        outf = join(outdir, 'phenology_dataframe.df')
        all_result_dic = {}
        pix_list_all = []

        for f in T.listdir(f_dir):
            if not f.endswith('.df'):
                continue
            df = T.load_df(join(f_dir, f))
            columns = df.columns
            column_list = []
            for col in columns:
                if col == 'pix':
                    continue
                column_list.append(col)
            for i, row in tqdm(df.iterrows(), total=len(df)):
                pix = row['pix']
                lon, lat = DIC_and_TIF().pix_to_lon_lat(pix)
                # if lat > 70:
                #     continue
                # address = Tools().lonlat_to_address(lon, lat)
                # print(address)
                for col in column_list:
                    dic_i = row[col]

                    dic_clean = {}
                    # print(dic_i)
                    # values_list=dic_i.values()
                    # values_list=list(values_list)
                    series = pd.Series(dic_i)
                    cap_series = self.cap(series)
                    # print(series)
                    # plt.plot(series)
                    # # plt.title(address)
                    # plt.plot(cap_series)
                    #
                    # plt.show()
                    for year in dic_i:
                        dic_clean[year] = cap_series[year]
                    if pix not in all_result_dic:
                        all_result_dic[pix] = {}

                    all_result_dic[pix][col] = dic_clean
            # convert to df
            df_all = T.dic_to_df(all_result_dic, 'pix')
            #save
            T.save_df(df_all, outf)
            T.df_to_excel(df_all, outf)



    def cap(self, x, quantile=(0.05, 0.95)):

        """盖帽法处理异常值
        Args：
            x：pd.Series列，连续变量
            quantile：指定盖帽法的上下分位数范围
        """

        # 生成分位数
        Q01, Q99 = x.quantile(quantile).values.tolist()

        # 替换异常值为指定的分位数
        if Q01 > x.min():
            x = x.copy()
            x.loc[x < Q01] = Q01

        if Q99 < x.max():
            x = x.copy()
            x.loc[x > Q99] = Q99

        return (x)

    def average_phenology(self, ):   #将多年物候期平均
        fdir_all = data_root + f'LAI/phenology/compose_annual_phenology/'
        for fdir in os.listdir(fdir_all):
            if not 'MCD' in fdir:
                continue

            outdir = data_root + f'LAI/phenology/average_phenology/{fdir}/'
            T.mkdir(outdir, force=True)
            outf = join(outdir, 'phenology_dataframe.df')

            all_result_dic = {}

            for f in T.listdir(fdir_all + fdir):
                if not f.endswith('.df'):
                    continue
                df = T.load_df(join(fdir_all,fdir, f))
                columns = df.columns
                column_list = []
                for col in columns:
                    if col == 'pix':
                        continue
                    column_list.append(col)

                pix_list = T.get_df_unique_val_list(df, 'pix')

                ########################################build dic##############################################################
                for pix in pix_list:
                    dic_i = {}
                    for col in column_list:
                        dic_i[col] = {}
                    all_result_dic[pix] = dic_i

                for i, row in tqdm(df.iterrows(), total=len(df)):
                    pix = row['pix']
                    lon, lat = DIC_and_TIF().pix_to_lon_lat(pix)
                    # address=Tools().lonlat_to_address(lon,lat)
                    # print(address)
                    for col in column_list:
                        dic_i = row[col]
                        # print(dic_i)
                        values = dic_i.values()
                        values = list(values)
                        value_mean = np.mean(values)
                        value_ = round(value_mean, 0)
                        value_std = np.std(values)
                        all_result_dic[pix][col] = value_

            df_all = T.dic_to_df(all_result_dic, 'pix')
            T.save_df(df_all, outf)
            T.df_to_excel(df_all, outf)
            np.save(outf, all_result_dic)

    def pick_daily_phenology(self):  # 转换格式 for example: early [100,150], peak [150,200], late [200,300]
        fdir_all = data_root + f'LAI/phenology/average_phenology/'
        for fdir in os.listdir(fdir_all):
            if not fdir.endswith('MCD'):
                continue
            outdir = data_root + f'LAI/phenology/pick_daily_phenology/{fdir}/'
            T.mkdir(outdir, force=True)
            outf = join(outdir, 'pick_daily_phenology.df')

            phenology_df = T.load_df(
                f'{fdir_all}/{fdir}/phenology_dataframe.df')

            early_dic = {}
            peak_dic = {}
            late_dic = {}
            all_result_dic = {}

            for i, row in tqdm(phenology_df.iterrows(), total=len(phenology_df)):
                pix = row['pix']
                all_result_dic[pix] = {}
                early_start = row['early_start']
                early_end = row['early_end']
                peak_start = row['early_end']
                peak_end = row['late_start']
                late_start = row['late_start']
                late_end = row['late_end']
                early_period = np.arange(int(early_start), int(early_end), 1)
                # print(early_period)
                peak_period = np.arange(int(early_end), int(late_start), 1)
                # print(peak_period)
                late_period = np.arange(int(late_start), int(late_end), 1)
                # print(late_period)
                all_result_dic[pix]['early'] = early_period
                all_result_dic[pix]['peak'] = peak_period
                all_result_dic[pix]['late'] = late_period
                all_result_dic[pix]['early_peak'] = np.concatenate((early_period, peak_period))
                all_result_dic[pix]['early_peak_late'] = np.concatenate((early_period, peak_period, late_period))
                # print(all_result_dic[pix])


            df_all = T.dic_to_df(all_result_dic, 'pix')
            T.save_df(df_all, outf)
            T.df_to_excel(df_all, outf)
            np.save(outf, all_result_dic)

    def pick_monthly_phenology(self):  # 转换格式 for example: early [100,150], peak [150,200], late [200,300]
        fdir_all = data_root + f'LAI/phenology/average_phenology/'
        for fdir in os.listdir(fdir_all):
            if not fdir.endswith('MCD'):
                continue
            outdir = data_root + f'LAI/phenology/pick_monthly_phenology/{fdir}/'
            T.mkdir(outdir, force=True)
            outf = join(outdir, 'pick_monthly_phenology.df')

            phenology_df = T.load_df(
                f'{fdir_all}/{fdir}/phenology_dataframe.df')

            early_dic = {}
            peak_dic = {}
            late_dic = {}
            all_result_dic = {}

            for i, row in tqdm(phenology_df.iterrows(), total=len(phenology_df)):
                pix = row['pix']
                all_result_dic[pix] = {}

                early_start = row['early_start_mon']
                early_end = row['early_end_mon']

                late_start = row['late_start_mon']
                late_end = row['late_end_mon']
                early_period= np.arange(int(early_start), int(early_end))
                early_peak_period = list(range(int(early_start), int(late_start)))
                peak_period=list(range(int(early_end), int(late_start)))
                late_period = list(range(int(late_start), int(late_end)+1))
                print(early_peak_period)
                print(peak_period)
                print(early_period)
                print(late_period)
                print('-------------------')
                # exit()
                all_result_dic[pix]['early_peak'] = early_peak_period
                all_result_dic[pix]['early'] = early_period
                all_result_dic[pix]['peak'] = peak_period
                all_result_dic[pix]['late'] = late_period

                # print(all_result_dic[pix])


            df_all = T.dic_to_df(all_result_dic, 'pix')
            T.save_df(df_all, outf)
            T.df_to_excel(df_all, outf)
            np.save(outf, all_result_dic)



    def plot_phenology(self):
        # df_f=data_root+r'MODIS_LAI_MOD15A2H\phenology\annual_phenology\\2015.df'
        df_f=data_root+r'Trendy\phenology\annual_phenology\MODIS\\2021.df'

        df=T.load_df(df_f)
        colunms='early_start'
        spatial_dic=T.df_to_spatial_dic(df,colunms)
        arr=DIC_and_TIF().pix_dic_to_spatial_arr(spatial_dic)
        plt.imshow(arr,vmin=100,vmax=160,cmap='jet')
        plt.colorbar()
        plt.show()


class frequency_analysis():  # Amplification and Stabilization analysis

    def __init__(self):

        # This class is used to calculate the structural equation model
        self.this_class_arr = result_root + 'Data_frame\\Frequency\\LAI3g_MCD_2003_2018\\MCD\\'
        self.this_class_tif = result_root + 'Data_frame\\Frequency\\LAI3g_MCD_2003_2018\\MCD\\'

        self.dff = self.this_class_arr + 'frequency_dataframe.df'

        Tools().mk_dir(self.this_class_arr, force=True)


        pass

    def run(self):

        ### 1.create frequency dataframe

        # df=self.pick_greening_year_frequency_heatmap()

        ## 2. add landcover and trend, row, and some attributes

        # call the function in the class of 'build_dataframe'

        # 3. plot frequency heatmap

        df, dff = self.__load_df()
        df_clean = self.clean_df(df)
        self.frenquency_heatmap(df_clean)

        ## 4. plot frequency bar
        # self.frenquency_heatmap_bar(df_clean)

        # 5. create spatial map of frequency of stabilization and amplification


        pass

    def __load_df(self):
        dff = self.dff
        df = T.load_df(dff)

        return df, dff
        # return df_early,dff

    def clean_df(self, df):
        df = df[df['row'] < 120]
        # df = df[df['HI_class'] == 'Humid']
        # df = df[df['HI_class'] == 'Dryland']
        df = df[df['max_trend'] < 10]

        df = df[df['landcover_GLC'] != 'Crop']

        return df


    def pick_greening_year_frequency_heatmap(self): # 通过pick years and calculate frequency

        f_early_peak_LAI = result_root + rf'\\detrend_zscore\\early_peak\\Trendy_ensemble.npy'
        f_late_LAI = result_root + rf'\detrend_zscore\\late\\Trendy_ensemble.npy'
        outdir = result_root + rf'Data_frame/Frequency/\\Trendy_ensemble///'
        outf = outdir + f'frequency_dataframe.df'
        T.mk_dir(outdir, force=1)
        dic_early_peak_LAI = dict(np.load(f_early_peak_LAI, allow_pickle=True, ).item())
        dic_late_LAI = dict(np.load(f_late_LAI, allow_pickle=True, ).item())
        # threshold_early_list=np.linspace(-2, 2, 21)
        #
        # threshold_late_list=np.linspace(-2, 2, 21)

        threshold_early_list = [0, 0.5, 1, 1.5, 2, 2.5, 3]

        threshold_late_list = [-3, -2.5, -2, -1.5, -1, -0.5, 0, 0.5, 1, 1.5, 2, 2.5, 3]

        all_result_dic={}


        for i in tqdm(range(len(threshold_early_list))):
            if i >= len(threshold_early_list) - 1:
                break

            for j in range(len(threshold_late_list)):
                if j >= len(threshold_late_list) - 1:
                    break

                early_threshold=threshold_early_list[i]
                late_threshold=threshold_late_list[j]

                spatial_dic={}
                for pix in dic_early_peak_LAI:

                    early_peak_LAI = dic_early_peak_LAI[pix]

                    # print(len(early_peak_LAI))
                    if not pix in dic_late_LAI:
                        continue
                    late_LAI=dic_late_LAI[pix]

                    early_condition1=early_peak_LAI > threshold_early_list[i]
                    early_condition2=early_peak_LAI < threshold_early_list[i + 1]
                    early_condition_intersect_index=np.logical_and(early_condition1, early_condition2)

                    index_early_peak_LAI = np.where(early_condition_intersect_index)
                    index_early_peak_LAI=np.array(index_early_peak_LAI)
                    index_early_peak_LAI=index_early_peak_LAI.flatten()

                    if threshold_late_list[j]>=0:
                        factor=1
                    else:
                        factor=-1
                    late_condition1=late_LAI > threshold_late_list[j]
                    late_condition2= late_LAI < threshold_late_list[j+1]


                    late_LAI_condition_intersect_index = np.logical_and(late_condition1, late_condition2)

                    index_late_LAI = np.where(late_LAI_condition_intersect_index)

                    intersect_index = np.intersect1d(index_early_peak_LAI, index_late_LAI)
                    if len(index_early_peak_LAI)==0:
                        continue

                    frequency=len(intersect_index)/len(index_early_peak_LAI)*100*factor



                    spatial_dic[pix] = frequency
                    column_name=f'{early_threshold:0.5f}-{late_threshold:0.5f}'
                    all_result_dic[column_name]=spatial_dic

        df=T.spatial_dics_to_df(all_result_dic)

        T.save_df(df,outf)
        T.df_to_excel(df,outf)
        return df

    def build_frequency_heatmap_dataframe(self,df, P_PET_fdir):


        build_dataframe().add_row(df)
        build_dataframe().add_NDVI_mask(df)
        build_dataframe().add_GLC_landcover_data_to_df(df)
        build_dataframe().add_max_trend_to_df(df)
        P_PET_dic =build_dataframe().P_PET_ratio(P_PET_fdir)
        P_PET_reclass_dic = build_dataframe(P_PET_fdir)
        df = T.add_spatial_dic_to_df(df, P_PET_reclass_dic, 'HI_class')
        pass


    def frenquency_heatmap(self,df):
        T.print_head_n(df, 10)

        # df = df.drop_duplicates(subset=['pix'])
        vals_dic = DIC_and_TIF().void_spatial_dic()
        regions = ['Humid', 'Dryland']
        cm=1/2.54

        for region in regions:
            plt.figure(figsize=(15*cm, 7*cm))

            df_temp=df[df['HI_class']==region]

            threshold_early_list = [0, 0.5, 1, 1.5, 2, 2.5, 3]

            threshold_late_list = [-3, -2.5, -2, -1.5, -1, -0.5, 0, 0.5, 1, 1.5, 2, 2.5, 3]

            threshold_late_list_reverse = threshold_late_list
            threshold_early_list_reverse = threshold_early_list[::-1]

            threshold_early_list_str = [f'{i:.5f}' for i in threshold_early_list]
            threshold_late_list_str = [f'{i:.5f}' for i in threshold_late_list]


            x_list = []
            y_list = []
            z_list = []

            for x in threshold_early_list_str:
                for y in threshold_late_list_str:
                    key=f'{x}-{y}'
                    if key not in df_temp.keys():
                        continue
                    vals = df_temp[key].to_list()
                    # plt.hist(vals,bins=20)
                    # plt.show()

                    vals = np.array(vals)
                    # vals[vals==0]=np.nan
                    vals_mean = np.nanmean(vals)
                    z_list.append(vals_mean)
                    x_list.append(x)
                    y_list.append(y)

            z_list=np.array(z_list)
            z_list=z_list.reshape(len(threshold_early_list_str)-1,len(threshold_late_list_str)-1)
            # z_list_T = z_list.T
            z_list_T = z_list
            z_list_T = z_list_T[::-1]
            label_matrix=abs(z_list_T)
            label_matrix=np.round(label_matrix,2)
            print(label_matrix)
            # np.save(result_root + rf'Data_frame\\Frequency\\LAI3g_MCD_2003_2018\\MCD_{region}.npy', label_matrix)
            # exit()


            ax=sns.heatmap(z_list_T, annot=label_matrix, linewidths=0.75,yticklabels=threshold_early_list_str,
                           xticklabels=threshold_late_list_str,cmap='RdBu',vmin=-15,vmax=15,
                           annot_kws={'fontsize': 8},
                           cbar_kws={'label': 'Frenquency (%)','ticks':[-15, -10,-5, 0, 5, 10,15]},fmt='.1f')
            threshold_early_list_str_format = [f'{i:.2f}' for i in threshold_early_list_reverse]
            threshold_late_list_str_format = [f'{i:.2f}' for i in threshold_late_list_reverse]

            ax.set_xticklabels(threshold_late_list_str_format, rotation=45, horizontalalignment='right')

            ax.set_yticklabels(threshold_early_list_str_format, rotation=0, horizontalalignment='right')
            cbar=ax.collections[0].colorbar
            cbar.ax.set_yticklabels([15, 10, 5, 0, 5, 10,15])
            # plt.tight_layout()


            plt.title(f'Trendy_{region}')

        plt.show()
        plt.close()
        #     plt.savefig(result_root + rf'Data_frame\\Frequency\\Trendy_{region}.pdf', dpi=300, )
        #     plt.close()

    def frenquency_heatmap_bar(self):

        fdir = join(data_root, 'Frequency/LAI3g')
        outdir = join(self.this_class_png, 'LAI3g')
        T.mk_dir(outdir)
        for f in T.listdir(fdir):
            arr = np.load(join(fdir, f))
            flag = 0
            strong_stabilization_sum_list = []
            weak_stabilization_sum_list = []
            amplification_sum_list = []
            for arr_i in arr:
                strong_stabilization = arr_i[:6]
                weak_stabilization = arr_i[6:12 - flag]
                amplification = arr_i[12 - flag:]
                flag += 1
                strong_stabilization_sum = np.sum(strong_stabilization)
                weak_stabilization_sum = np.sum(weak_stabilization)
                amplification_sum = np.sum(amplification)

                strong_stabilization_sum_list.append(strong_stabilization_sum)
                weak_stabilization_sum_list.append(weak_stabilization_sum)
                amplification_sum_list.append(amplification_sum)
            strong_stabilization_sum_list = np.array(strong_stabilization_sum_list)
            weak_stabilization_sum_list = np.array(weak_stabilization_sum_list)
            amplification_sum_list = np.array(amplification_sum_list)

            plt.bar(np.arange(len(arr)), strong_stabilization_sum_list, label='strong_stabilization')
            plt.bar(np.arange(len(arr)), weak_stabilization_sum_list, bottom=strong_stabilization_sum_list,
                    label='weak_stabilization')
            plt.bar(np.arange(len(arr)), amplification_sum_list,
                    bottom=strong_stabilization_sum_list + weak_stabilization_sum_list, label='amplification')
            # plt.legend()
            plt.title(f)
            outf = join(outdir, f.replace('.npy', '.pdf'))
            plt.savefig(outf)
            plt.close()
            # plt.show()
        T.open_path_and_file(outdir)

    def spatial_frequency(self):
        Ter = xymap.Ternary_plot(
            top_color=(10, 94, 0),
            left_color=(0, 30, 210),
            # left_color=(119,0,188),
            right_color=(230, 0, 230),
            # center_color=(85,85,85),
            center_color=(230, 230, 230),
            # center_color=(255,255,255),
        )
        rgb_arr = Ter.rgb_arr

        # plt.imshow(rgb_arr)
        # plt.show()
        outdir = join(self.this_class_tif,'frequency_rgba_LAI3g')
        fdir_early = join(data_root,'LAI3g_MCD_2003_2018/early_peak')
        fdir_late = join(data_root,'LAI3g_MCD_2003_2018/late')
        for f in T.listdir(fdir_early):
            # if not 'MCD' in f:
            #     continue
            outdir_i = join(outdir,f.replace('.npy',''))
            T.mk_dir(outdir_i,force=True)
            fpath_early = join(fdir_early,f)
            fpath_late = join(fdir_late,f)
            early_dict = T.load_npy(fpath_early)
            late_dict = T.load_npy(fpath_late)
            result_dict = {}
            for pix in tqdm(early_dict,desc=f):
                early_vals = early_dict[pix]
                if not pix in late_dict:
                    continue
                late_vals = late_dict[pix]
                father = 0
                son_amplification = 0
                son_weak_stabilization = 0
                son_strong_stabilization = 0
                for i in range(len(early_vals)):
                    early_val = early_vals[i]
                    late_val = late_vals[i]
                    if early_val < 0:
                        continue
                    father += 1
                    if late_val > early_val:
                        son_amplification += 1
                    elif late_val < early_val and late_val > 0:
                        son_weak_stabilization += 1
                    else:
                        son_strong_stabilization += 1
                if father == 0:
                    continue
                ratio_amplification = son_amplification/father
                ratio_weak_stabilization = son_weak_stabilization/father
                ratio_strong_stabilization = son_strong_stabilization/father
                result_dict[pix] = {
                    'ratio_amplification':ratio_amplification,
                    'ratio_weak_stabilization':ratio_weak_stabilization,
                    'ratio_strong_stabilization':ratio_strong_stabilization,
                }
            if len(result_dict) == 0:
                continue
            df = T.dic_to_df(result_dict,'pix')
            cols = ['ratio_amplification','ratio_weak_stabilization','ratio_strong_stabilization']
            # cols = []
            arr_list = []
            for col in cols:
                spatial_dict = T.df_to_spatial_dic(df,col)
                arr = DIC_and_TIF().pix_dic_to_spatial_arr(spatial_dict)
                arr = np.array(arr)
                ##### interpolation
                window = 3
                new_arr = []
                for i in tqdm(range(len(arr))):
                    new_arr_i = []
                    for j in range(len(arr[0])):
                        val = arr[i, j]
                        if np.isnan(val):
                            val = np.nanmean(arr[i - window:i + window + 1, j - window:j + window + 1])
                        new_arr_i.append(val)
                    new_arr.append(new_arr_i)
                new_arr = np.array(new_arr)


                arr_list.append(new_arr)

                # arr_list.append(arr)

            color_matrix = []

            s1_matrix = []
            s2_matrix = []
            s3_matrix = []

            for i in range(len(arr_list[0])):
                color_matrix_i = []
                s1_matrix_i = []
                s2_matrix_i = []
                s3_matrix_i = []
                for j in range(len(arr_list[0][0])):
                    s1 = arr_list[0][i,j]
                    s2 = arr_list[1][i,j]
                    s3 = arr_list[2][i,j]

                    s1_matrix_i.append(s1)
                    s2_matrix_i.append(s2)
                    s3_matrix_i.append(s3)


                    if np.isnan(s1) or np.isnan(s2) or np.isnan(s3):
                        color = (0, 0, 0, 0)
                        color_matrix_i.append(color)
                        continue

                    # print(s1,s2,s3)

                    color = Ter.get_color(s1,s2,s3)
                        # r, g, b, w = 0, 0, 0, 0
                        # color_matrix_i.append(np.array([r, g, b, w]))
                        # continue
                    # color = Ter.get_color(s1,s2,s3)
                    r,g,b = color
                    r,g,b = int(r*255),int(g*255),int(b*255)
                    w = 255
                    if r==255 and g==255 and b==255:
                        print(s1,s2,s3)
                    color_matrix_i.append(np.array([r,g,b,w]))
                    # color_matrix_i.append(np.array([r3, g3, b3,255]))
                    # color_matrix_i.append(np.array([r1,g1,b1,255]))
                # exit()
                s1_matrix.append(s1_matrix_i)
                s2_matrix.append(s2_matrix_i)
                s3_matrix.append(s3_matrix_i)
                color_matrix.append(color_matrix_i)
            s1_matrix = np.array(s1_matrix,dtype=float)
            s2_matrix = np.array(s2_matrix,dtype=float)
            s3_matrix = np.array(s3_matrix,dtype=float)
            color_matrix = np.array(color_matrix)
            outf = join(outdir_i,'frequency.tif')
            outf_s1 = join(outdir_i,'s1.tif')
            outf_s2 = join(outdir_i,'s2.tif')
            outf_s3 = join(outdir_i,'s3.tif')
            DIC_and_TIF().arr_to_tif(s1_matrix,outf_s1)
            DIC_and_TIF().arr_to_tif(s2_matrix,outf_s2)
            DIC_and_TIF().arr_to_tif(s3_matrix,outf_s3)
            # T.open_path_and_file(outdir_i)
            legend_arr = Ter.rgb_arr
            plt.imshow(legend_arr)
            plt.axis('off')
            plt.axis('equal')
            legend_f = join(outdir_i,'legend.pdf')
            plt.savefig(legend_f)

            img = Image.fromarray(color_matrix.astype('uint8'), 'RGBA')
            img.save(outf)
            raster = gdal.Open(outf)
            geotransform = raster.GetGeoTransform()
            originX = DIC_and_TIF().originX
            originY = DIC_and_TIF().originY
            pixelWidth = DIC_and_TIF().pixelWidth
            pixelHeight = DIC_and_TIF().pixelHeight

            raster.SetGeoTransform((originX, pixelWidth, 0, originY, 0, pixelHeight))
            outRasterSRS = osr.SpatialReference()

            # outRasterSRS.ImportFromEPSG(4326)
            # outRasterSRS.ImportFromEPSG(projection)
            # raster.SetProjection(outRasterSRS.ExportToWkt())
            raster.SetProjection('EPSG:4326')
            # T.open_path_and_file(outdir_i)
            # exit()
        T.open_path_and_file(outdir)
        # exit()

    def get_raster_projections(self, rasterfn):
        '''
        get raster projection
        Agrs:
            rasterfn: tiff file path
        Returns:
            projection: projection of the raster
        '''
        raster = gdal.Open(rasterfn)
        projection = raster.GetProjection()
        return projection


class SEM_wen:
    def __init__(self):
        # This class is used to calculate the structural equation model
        self.this_class_arr = result_root + '\Data_frame\detrend_zscore_new\\'
        self.dff = self.this_class_arr + 'detrend_zscore_new.df'
        self.outdir = result_root + 'SEM3//'
        T.mkdir(self.outdir, force=True)

        pass

    def run(self):
        df, dff = self.__load_df()
        des = self.model_description_not_detrend_new()

        df_clean = self.clean_df(df)
        self.SEM_model(df_clean, des)
        pass

    def __load_df(self):
        dff = self.dff
        df = T.load_df(dff)

        return df, dff
        # return df_early,dff

    def clean_df(self, df):
        df = df[df['row'] < 120]
        # df = df[df['HI_class'] == 'Humid']
        df = df[df['HI_class'] == 'Dryland']
        df = df[df['max_trend'] < 10]
        df = df[df['early_peak_MCD'] > 0]
        ## late <early
        # df=df[df['late_MCD']>df['early_peak_MCD']] ###
        # df=df[df['late_MCD']<0]
        # df = df[df['detrend_late_MODIS_LAI_zscore'] > 0]

        df = df[df['landcover_GLC'] != 'Crop']

        return df

    def model_description_not_detrend(self):
        desc_water_limited_SMroot = '''
                            # regressions

                            early_peak_MCD~early_Temp+early_precip

                            peak_SMroot~  early_peak_MCD+peak_precip

                            late_MCD ~ peak_SMroot + late_Temp
                            late_MCD~peak_precip


                            # residual correlations
                             early_peak_MCD~~early_peak_MCD
                                peak_SMroot~~peak_SMroot
                                late_MCD~~late_MCD

                                early_peak_MCD~~early_Temp
                                early_peak_MCD~~early_precip
                                peak_SMroot~~early_peak_MCD
                                peak_SMroot~~peak_precip
                                late_MCD~~peak_SMroot
                                late_MCD~~late_Temp
                                late_MCD~~peak_precip

                            '''

        desc_energy_limited_SMroot = '''
                                    # regressions

                                    early_peak_MCD~early_Temp+early_precip

                                    peak_SMroot~  early_peak_MCD+peak_precip

                                    late_MCD ~ peak_SMroot + late_Temp
                                    late_MCD~peak_precip


                                    # residual correlations
                                     early_peak_MCD~~early_peak_MCD
                                        peak_SMroot~~peak_SMroot
                                        late_MCD~~late_MCD

                                        early_peak_MCD~~early_Temp
                                        early_peak_MCD~~early_precip
                                        peak_SMroot~~early_peak_MCD
                                        peak_SMroot~~peak_precip
                                        late_MCD~~peak_SMroot
                                        late_MCD~~late_Temp
                                        late_MCD~~peak_precip

                                    '''

        return desc_water_limited_SMroot

    def model_description_not_detrend_new(self):
        desc_all_limited_SMroot = '''
                             # regressions

                             early_peak_MCD~early_Temp+early_precip

                             late_SMroot~  early_peak_MCD+late_Temp+peak_precip

                             late_MCD ~ late_SMroot + late_Temp+late_precip


                             # residual correlations
                              early_peak_MCD~~early_peak_MCD
                                 late_SMroot~~late_SMroot
                                 late_MCD~~late_MCD

                                 early_peak_MCD~~early_Temp
                                 early_peak_MCD~~early_precip
                                 late_SMroot~~early_peak_MCD

                                 late_MCD~~late_SMroot
                                 late_SMroot~~late_Temp
                                 late_MCD~~late_Temp

                                 late_SMroot~~peak_precip

                                    late_MCD~~late_precip


                             '''

        return desc_all_limited_SMroot

    def SEM_model(self, df, desc):
        mod = semopy.Model(desc)
        res = mod.fit(df)

        result = mod.inspect()
        T.print_head_n(result)
        outf = self.outdir + f'water_limited_MCD'
        T.save_df(result, outf + '.df')
        T.df_to_excel(result, outf + '.xlsx')

        outf = self.outdir + 'water_limited_MCD'
        semopy.report(mod, outf)


class Stabilization_amplification_longterm_trends:

    def __init__(self):

        pass

    def plot_feedback_vs_trend(self):
        dff=result_root+rf'Data_frame\zscore_result_statistical_annual\frequency_temporal_change_TRENDY_individual_statistic\\result_new.df'
        df=T.load_df(dff)
        marker_list = ['*','o', 's', 'D', 'v', 'p', 'P', '^', 'X', 'd', '<', '>']


        color_list = T.gen_colors(12)

        ##plot x =feedback and y = trend
        periods = ['early_peak_late','late']
        product_list = ['MCD', 'CABLE-POP_S2_lai', 'CLASSIC_S2_lai', 'CLM5', 'IBIS_S2_lai',
            'ISAM_S2_LAI', 'ISBA-CTRIP_S2_lai', 'JSBACH_S2_lai',
            'LPX-Bern_S2_lai', 'VISIT_S2_lai',  ]
        region_list=['Humid','Dryland']

        for region in region_list:

            for period in periods:
                x_list = []
                y_list = []
                label_list = []
                p_value_list_sta=[]
                p_value_list_trend=[]
                flag = 0
                for variable in product_list:

                    key=f'{region}-{variable}'
                    df_pick=df[df['model']==key]
                    y=df_pick[f'k_value_{period}'].to_list()
                    x=df_pick[f'a_strong_stab'].to_list()
                    x=x[0]*100
                    y=y[0]

                    p_value_sta=df_pick[f'p_strong_stab'].to_list()
                    p_value_trend=df_pick[f'p_value_{period}'].to_list()
                    x_list.append(x)

                    y_list.append(y)
                    p_value_list_sta.append(p_value_sta)
                    p_value_list_trend.append(p_value_trend)

                    label_list.append(f'{region}-{variable}-{period}')
                centimeter = 2.54
                plt.figure(figsize=(9/centimeter, 7/centimeter))

                for i in range(len(x_list)):
                    x=x_list[i]
                    y=y_list[i]
                    label=label_list[i]
                    p_value_trend=p_value_list_trend[i]

                    p_value_sta=p_value_list_sta[i]
                    plt.scatter(x,y,label=label,marker=marker_list[flag],color=color_list[flag])
                    plt.text(x, y, f'P={p_value_trend[0]:0.2f}\nP={p_value_sta[0]:0.2f}', fontsize=6, color='black')

                    flag+=1

                plt.title(f'{region}-{period}')
                plt.xlabel('strong_stabilization_feedback_trend (%/year)')
                plt.ylabel('interannual_growing_season_trend(/year)')
                plt.legend()
                plt.tight_layout()
                outdir=result_root+rf'\\Data_frame\zscore_result_statistical_annual\frequency_temporal_change_TRENDY_individual_statistic\\'
                outf=join(outdir,f'{region}_{period}.pdf')
                plt.savefig(outf)
                plt.close()



    def plot_time_series_zscore(self):  ###plot time series
        f = result_root + rf'\\Data_frame\zscore_result_statistical_annual\\zscore_result_statistical_annual_average_new.npy'
        dic = T.load_npy(f)
        period_name = ['early_peak', 'late', 'early_peak_late']


        product_list = ['MCD', 'average', 'CABLE-POP_S2_lai', 'CLASSIC_S2_lai', 'CLM5', 'IBIS_S2_lai',
                        'ISAM_S2_LAI', 'ISBA-CTRIP_S2_lai', 'JSBACH_S2_lai',
                        'LPX-Bern_S2_lai', 'VISIT_S2_lai', 'YIBs_S2_Monthly_lai', ]
        color_list = ['green', 'black']
        color_list.extend('silver' for i in range(len(product_list) - 2))
        linewidth_list = [2, 2, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5,
                          0.5]

        centimeter = 1 / 2.54


        fig = plt.figure(figsize=(18 * centimeter, 12 * centimeter))
        i = 1

        for region in ['Humid', 'Dryland']:

            for period in period_name:
                ax = fig.add_subplot(2, 3, i)

                flag = 0
                for variable in product_list:

                    color = color_list[flag]
                    linewidth = linewidth_list[flag]
                    if flag >= 2:
                        zorder = 0
                    else:
                        zorder = 1

                    flag += 1
                    key = f'{region}_{period}_{variable}'
                    result_i = dic[key]
                    mean_value_yearly = result_i['mean_value_yearly']
                    # up_list = result_i['up_list']
                    # bottom_list = result_i['bottom_list']
                    fit_value_yearly = result_i['fit_value_yearly']
                    k_value = result_i['k_value']
                    p_value = result_i['p_value']
                    print(f'{region}_{variable}', 'k={:0.2f},p={:0.4f}'.format(k_value, p_value))
                    yearlist=range(2003,2022)

                    plt.plot(yearlist,mean_value_yearly, label=variable, c=color, zorder=zorder, linewidth=linewidth)
                    plt.plot(yearlist,fit_value_yearly, linestyle='--', label='k={:0.2f},p={:0.2f}'.format(k_value, p_value),
                             c=color, linewidth=linewidth)
                    # print(f'{region}_{variable}','k={:0.2f},p={:0.4f}'.format(k_value, p_value))
                    # plt.fill_between(range(len(mean_value_yearly)), up_list, bottom_list, alpha=0.1, zorder=-1,
                    #                  color=color)
                    #### show text p value trend only show Trendy_ensemble and MCD
                    if variable == 'average' or variable == 'MCD':
                        ## position of text
                        x = 0
                        y = mean_value_yearly[0]+0.7
                        # plt.text(x, y, 'k={:0.2f},p={:0.2f}'.format(k_value, p_value), fontsize=10, color=color)


                plt.ylabel('zscore')
                plt.xlabel('year')
                major_xticks = np.arange(2003, 2022, 5)
                plt.xticks(major_xticks, rotation=45)
                plt.title(f'{period}_{region}')

                # major_yticks = np.arange(-10, 15, 5)
                major_yticks = np.arange(-0.8, 0.9, 0.4)
                plt.ylim(-0.8, 0.8)
                # major_ticks = np.arange(0, 40, 5)  ### 根据数据长度修改这里
                ax.set_xticks(major_xticks)
                ax.set_yticks(major_yticks)
                plt.grid(which='major', alpha=0.5)
                plt.tight_layout()
                i = i + 1
        outdir = result_root + rf'\\Data_frame\zscore_result_statistical_annual\\'
        T.mk_dir(outdir, force=1)
        outf = outdir + 'zscore_result_statistical_annual_average_new.pdf'
        plt.savefig(outf)
        plt.close()


        plt.show()



