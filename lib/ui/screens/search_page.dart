import 'package:flutter/material.dart';
import 'package:leafspec/constants.dart';
import 'package:leafspec/models/plants.dart';
import 'package:leafspec/ui/screens/widgets/plant_widget.dart';
import 'package:page_transition/page_transition.dart';
import 'package:leafspec/ui/screens/detail_page.dart';

class SearchPage extends StatefulWidget {
  final List<Plant> addedToCartPlants;
  const SearchPage({super.key, required this.addedToCartPlants});

  @override
  State<SearchPage> createState() => _SearchPageState();
}

class _SearchPageState extends State<SearchPage> {
  TextEditingController _searchController = TextEditingController();
  List<Plant> plantList = Plant.plantList;
  List<Plant> filteredPlantList = [];

  @override
  void initState() {
    super.initState();
    filteredPlantList = plantList; // Initially show all plants
    _searchController.addListener(_filterPlants);
  }

  @override
  void dispose() {
    _searchController.removeListener(_filterPlants);
    _searchController.dispose();
    super.dispose();
  }

  void _filterPlants() {
    String query = _searchController.text.toLowerCase();
    setState(() {
      filteredPlantList = plantList.where((plant) {
        return plant.plantName.toLowerCase().contains(query); // Filter by name
      }).toList();
    });
  }

  @override
  Widget build(BuildContext context) {
    Size size = MediaQuery.of(context).size;

    return Scaffold(
      body: SingleChildScrollView(
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Container(
              padding: const EdgeInsets.only(top: 20),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceAround,
                children: [
                  Container(
                    padding: const EdgeInsets.symmetric(
                      horizontal: 16.0,
                    ),
                    width: size.width * .9,
                    decoration: BoxDecoration(
                      color: Constants.primaryColor.withOpacity(.1),
                      borderRadius: BorderRadius.circular(20),
                    ),
                    child: Row(
                      crossAxisAlignment: CrossAxisAlignment.center,
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Icon(
                          Icons.search,
                          color: Colors.black54.withOpacity(.6),
                        ),
                        Expanded(
                          child: TextField(
                            controller: _searchController,
                            decoration: const InputDecoration(
                              hintText: 'Search Plant',
                              border: InputBorder.none,
                              focusedBorder: InputBorder.none,
                            ),
                          ),
                        ),
                        Icon(
                          Icons.mic,
                          color: Colors.black54.withOpacity(.6),
                        ),
                      ],
                    ),
                  )
                ],
              ),
            ),
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 12),
              height: size.height * .75,
              child: filteredPlantList.isEmpty
                  ? Center(
                      child: Text(
                        'No plants found',
                        style: TextStyle(color: Colors.grey, fontSize: 16),
                      ),
                    )
                  : ListView.builder(
                      itemCount: filteredPlantList.length,
                      scrollDirection: Axis.vertical,
                      physics: const BouncingScrollPhysics(),
                      itemBuilder: (BuildContext context, int index) {
                        return GestureDetector(
                          onTap: () {
                            Navigator.push(
                              context,
                              PageTransition(
                                child: DetailPage(
                                    plantId: filteredPlantList[index].plantId),
                                type: PageTransitionType.bottomToTop,
                              ),
                            );
                          },
                          child: PlantWidget(
                              index: index, plantList: filteredPlantList),
                        );
                      },
                    ),
            ),
          ],
        ),
      ),
    );
  }
}
