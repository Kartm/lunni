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
};
