import { HomePage } from "../pages/home";
import { MergerPage } from "../pages/merger";

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
