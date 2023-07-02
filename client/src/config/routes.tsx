import { AnalysisPage } from "../components/pages/analysis";
import { HomePage } from "../components/pages/home";
import { MergerPage } from "../components/pages/merger";

export const routes = {
  "/": {
    component: <HomePage />,
    title: "Home",
  },
  "/merger": {
    component: <MergerPage />,
    title: "Merger",
  },
  "/analysis": {
    component: <AnalysisPage />,
    title: "Analysis",
  },
};
