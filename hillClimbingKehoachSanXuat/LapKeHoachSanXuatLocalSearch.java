package localsearch.applications;

import localsearch.constraints.basic.Implicate;
import localsearch.constraints.basic.LessOrEqual;
import localsearch.constraints.basic.NotEqual;
import localsearch.functions.basic.FuncMult;
import localsearch.functions.basic.FuncPlus;
import localsearch.functions.sum.SumFun;
import localsearch.model.ConstraintSystem;
import localsearch.model.IFunction;
import localsearch.model.LocalSearchManager;
import localsearch.model.VarIntLS;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Random;
import java.util.Scanner;
public class LapKeHoachSanXuatLocalSearch {
    // Doi tuong model
    LocalSearchManager mgr;
    VarIntLS[] X;
    ConstraintSystem S;
    IFunction muctieu;
    //
    int n, A, C;
    int[] f;
    int[] a;
    int[] c;
    int[] m;
    class AssignMove {
        int i;
        int v;
        public AssignMove(int i, int v) {
            this.i = i; this.v = v;
        }
    }
    public void hillClimbing(ConstraintSystem c, int maxIter, int[] f, IFunction muctieu) {
        VarIntLS[] y = c.getVariables();
        int[] bestSolution = new int[y.length];
        int fmax = Integer.MIN_VALUE;
        ArrayList<AssignMove> cand = new ArrayList<AssignMove>();
        Random R = new Random();
        int it = 0;
        while(it < maxIter) {
            cand.clear();
            int maxDelta = Integer.MAX_VALUE;
            int minMT = Integer.MIN_VALUE;
            for(int i = 0; i < y.length; i++) {
//                for(int v = y[i].getValue(); v <= y[i].getMaxValue(); v++) {
                for(int v = y[i].getMinValue(); v <= y[i].getMaxValue(); v++) {
                    int d = c.getAssignDelta(y[i], v);
                    int mt = muctieu.getAssignDelta(y[i],v);
                    if(d < maxDelta ) {
                        cand.clear();
                        cand.add(new AssignMove(i, v));
                        maxDelta = d;
                        minMT = mt;
                    }else if(d == maxDelta && mt>=minMT) {
                        cand.add(new AssignMove(i, v));
                    }
                }
            }
            System.out.println(muctieu.getValue());
            int idx = R.nextInt(cand.size());
            AssignMove m = cand.get(idx);
            y[m.i].setValuePropagate(m.v);
            it++;
        }
        System.out.print("Giai phap "+c.violations()+" violations, loi nhuan "+ muctieu.getValue() + ": ");
        for(int i=0;i<y.length;i++){
            bestSolution[y[i].getID()] = y[i].getValue();
        }
        for(int i =0 ;i<y.length;i++){
            System.out.print(bestSolution[i]);
            System.out.print(' ');
        }
    }
    public void initialize(String file) {
        File fl = new File(file);
        try {
            Scanner reader = new Scanner(fl);
            n = reader.nextInt();
            A = reader.nextInt();
            C = reader.nextInt();
            f = new int[n];
            a = new int[n];
            c = new int[n];
            m = new int[n];
            for (int i = 0; i < n; i++) {
                c[i] = reader.nextInt();
            }
            for (int i = 0; i < n; i++) {
                a[i] = reader.nextInt();
            }
            for (int i = 0; i < n; i++) {
                f[i] = reader.nextInt();
            }
            for (int i = 0; i < n; i++) {
                m[i] = reader.nextInt();
            }
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public void stateModel() {
        mgr = new LocalSearchManager();
        X = new VarIntLS[n];
        for (int i = 0; i < n; i++) {
            int maxC = C / c[i];
            int maxA = A / a[i];
            int max = (maxC > maxA) ? maxA : maxC;
            X[i] = new VarIntLS(mgr, 0, max);
        }
        S = new ConstraintSystem(mgr);
        IFunction plus = new FuncPlus(new FuncMult(X[0], c[0]), 0);
        for (int i = 1; i < n; i++) {
            plus = new FuncPlus(new FuncMult(X[i], c[i]), plus);
        }
        S.post(new LessOrEqual(plus, C));
        for (int i = 0; i < n; i++) {
            S.post(new Implicate(new NotEqual(X[i],0),new LessOrEqual(m[i], X[i])));
        }
        for (int i = 0; i < n; i++) {
            S.post(new LessOrEqual(new FuncMult(X[i], a[i]), A));
        }
        IFunction [] mt = new IFunction[n];
        for(int i=0; i<n; i++){
            mt[i] = new FuncPlus(X[i],f[i]);
        }
        muctieu = new SumFun(mt);
        mgr.close();
    }

    public static void main(String[] agrs) {
        LapKeHoachSanXuatLocalSearch task = new LapKeHoachSanXuatLocalSearch();
        task.initialize("/home/ubtur/Desktop/20202/toi_uu_lap_ke_hoach/Project/planningoptimization/data/LapKeHoachSX/data_10.txt");
        task.stateModel();
        task.hillClimbing(task.S, 10000, task.f,task.muctieu);
    }
}
